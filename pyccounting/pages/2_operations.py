import datetime

import numpy as np
import pandas as pd
import streamlit as st
from sqlalchemy.orm import Session

from pyccounting import db, display, widgets

CATEGORIES = [
    "restaurant & bars",
    "groceries",
    "travel",
    "housing",
    "culture",
    "sport",
    "daily life",
    "clothes",
    "health",
    "salary",
    "reimbursement",
    "transfer",
    "taxes",
    "other",
]

anonymous_mode: bool = widgets.anonymous_mode()
dates: tuple[datetime.date, datetime.date] = widgets.dates()
accounts: list[str] = widgets.accounts()
types: list[str] = widgets.types()
widgets.reset()

st.write("### Importation")

account = st.radio("Account:", ("bnp", "fortuneo"))
uploaded_file = st.file_uploader(label="Upload a file:", type=["csv", "xls"])

if uploaded_file is not None:

    if account == "bnp":
        sep = ","
        df_input: pd.DataFrame = pd.read_csv(uploaded_file, sep=sep)
    elif account == "fortuneo":
        sep = ";"
        df_input = pd.read_csv(uploaded_file, sep=sep)
        df_input = df_input.iloc[::-1]  # reverse the order of the DataFrame
    else:
        raise ValueError

    st.dataframe(df_input)

    df = db.get_df(accounts=[account], sort_by_date=True)
    id_: int = 1 if df.empty else df.iloc[-1]["id_"] + 1

    with Session(db.engine) as session:
        category_rules = session.query(db.CategoryRule).all()

        for _, row in df_input.iterrows():
            if account == "bnp":
                label = row["Libelle operation"]
                date = datetime.datetime.strptime(row["Date operation"], "%d/%m/%Y").date()
                amount = float(row["Montant operation en euro"].replace(",", "."))
            elif account == "fortuneo":
                label = row["libellé"]
                date = datetime.datetime.strptime(row["Date opération"], "%d/%m/%Y").date()
                if row["Débit"] and row["Crédit"] is np.nan:
                    amount = float(row["Débit"].replace(",", "."))
                elif row["Crédit"] and row["Débit"] is np.nan:
                    amount = float(row["Crédit"].replace(",", "."))
                else:
                    raise ValueError
            else:
                raise ValueError

            operation = db.Operation(
                id_=id_,
                account=account,
                label=label,
                date=date,
                amount=amount,
                category="",
            )
            operation.apply_category_rules(category_rules=category_rules)
            session.add(operation)
            id_ += 1

        session.commit()
        st.write(f"{len(df_input.index)} operations added.")

st.write("### All operations")

df = db.get_df(
    accounts=accounts,
    types=types,
    sort_by_date=True,
    dates=dates,
)

if df.empty:
    st.write("There's nothing to see, here! ;)")

else:
    st.write(f"{len(df.index)} operations:")
    display.table(df=df, anonymous_mode=anonymous_mode)

st.write("### Categories")

df = db.get_df(
    accounts=accounts,
    types=types,
    sort_by_date=True,
    dates=dates,
    categories=[""],
)

if df.empty:
    st.write("There's nothing to see, here! ;)")

else:
    st.write(f"The following {len(df.index)} operations have no category:")
    display.table(df=df, anonymous_mode=anonymous_mode)

    with st.form("category_rule"):
        st.write("You can add a new category rule:")
        kwargs = {
            "category": st.selectbox("Select a category:", CATEGORIES),
            "content": st.text_input("Add a content:"),
        }
        if st.form_submit_button("Submit"):
            with Session(db.engine) as session:
                category_rule = db.CategoryRule(**kwargs)
                session.add(category_rule)

                operations = session.query(db.Operation).filter(db.Operation.category == "").all()
                for operation in operations:
                    operation.apply_category_rules(category_rules=[category_rule])

                session.commit()

    with st.form("category_selection"):
        st.write("You can manually mark the remaining operations:")
        category = st.selectbox("Select a category: ", CATEGORIES)
        with Session(db.engine) as session:
            operation_labels = [
                operation.label
                for operation in session.query(db.Operation)
                .filter(db.Operation.category == "")
                .all()
            ][:25]
        checks = {}
        for i, operation_label in enumerate(operation_labels):
            checks[operation_label] = st.checkbox(
                label=operation_label,
                value=False,
                key=f"{i}_{operation_label}",
            )

        if st.form_submit_button("Submit"):
            with Session(db.engine) as session:
                for operation in (
                    session.query(db.Operation).filter(db.Operation.category == "").all()
                ):
                    if operation.label in checks and checks[operation.label]:
                        operation.category = category

                session.commit()
