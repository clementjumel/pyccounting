import datetime

import numpy as np
import pandas as pd
import streamlit as st
from sqlalchemy.orm import Session

from pyccounting import db, display, widgets

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
        for _, row in df_input.iterrows():
            if account == "bnp":
                type_ = row["Type operation"]
                label = row["Libelle operation"]
                date = datetime.datetime.strptime(row["Date operation"], "%d/%m/%Y").date()
                amount = float(row["Montant operation en euro"].replace(",", "."))
            elif account == "fortuneo":
                type_ = "unknown"
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
                type_=type_,
                label=label,
                date=date,
                amount=amount,
            )
            session.add(operation)
            id_ += 1

        session.commit()

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
    display.table(df=df, anonymous_mode=anonymous_mode)
