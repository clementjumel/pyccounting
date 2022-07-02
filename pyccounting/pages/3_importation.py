import datetime
import json

import numpy as np
import pandas as pd
import streamlit as st
from sqlalchemy.orm import Session

from pyccounting import db, widgets

account = st.selectbox("Account", ("bnp", "fortuneo"))
uploaded_file = st.file_uploader(label="Upload a file", type=["csv", "xls"])
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

    df: pd.DataFrame = db.get_df(sort_by_date=True)
    df = df.loc[df["account"] == account]
    if df.empty:
        id_: int = 1
        with open("data/start_amounts.json") as file:
            amount: float = json.load(file)[account]["amount"]
    else:
        series_latest_operation: pd.Series = df.iloc[-1]
        id_ = series_latest_operation["id_"] + 1
        amount = series_latest_operation["end_amount"]

    with Session(db.engine) as session:
        for _, row in df_input.iterrows():
            if account == "bnp":
                type_ = row["Type operation"]
                label = row["Libelle operation"]
                date = datetime.datetime.strptime(row["Date operation"], "%d/%m/%Y").date()
                operation_amount = float(row["Montant operation en euro"].replace(",", "."))
            elif account == "fortuneo":
                type_ = "unknown"
                label = row["libellé"]
                date = datetime.datetime.strptime(row["Date opération"], "%d/%m/%Y").date()
                if row["Débit"] and row["Crédit"] is np.nan:
                    operation_amount = float(row["Débit"].replace(",", "."))
                elif row["Crédit"] and row["Débit"] is np.nan:
                    operation_amount = float(row["Crédit"].replace(",", "."))
                else:
                    raise ValueError
            else:
                raise ValueError

            end_amount = round(amount + operation_amount, 2)
            operation = db.Operation(
                id_=id_,
                account=account,
                type_=type_,
                label=label,
                date=date,
                start_amount=amount,
                operation_amount=operation_amount,
                end_amount=end_amount,
            )
            session.add(operation)
            id_ += 1
            amount = end_amount

        session.commit()

widgets.reset()
