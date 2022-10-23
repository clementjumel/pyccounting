import datetime

import numpy as np
import pandas as pd
import streamlit as st
from sqlalchemy.orm import Session

from pyccounting import initialize, orm, widgets

initialize.initialize()

dates: tuple[datetime.date, datetime.date] = widgets.dates()
accounts: list[str] = widgets.accounts()
types: list[str] = widgets.types()
category_names: list[str] = widgets.categories()

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

    df = orm.get_df(accounts=[account], sort_by_date=True)
    idx: int = 1 if df.empty else df.iloc[-1]["idx"] + 1

    with Session(orm.engine) as session:
        category_rules = session.query(orm.CategoryRule).all()

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

            operation = orm.Operation(
                idx=idx,
                account=account,
                label=label,
                date=date,
                amount=amount,
                category_name="none",
            )
            operation.find_category_name(category_rules=category_rules)
            session.add(operation)
            idx += 1

        session.commit()
        st.write(f"{len(df_input.index)} operations added.")

st.write("### All operations")

df = orm.get_df(
    accounts=accounts,
    types=types,
    sort_by_date=True,
    dates=dates,
    category_names=category_names,
)

st.write(f"{len(df.index)} operations:")
columns = ["amount", "account", "label", "category_name"]

st.dataframe(df[columns])
