import datetime
import json

import numpy as np
import pandas as pd
import streamlit as st
from sqlalchemy.orm import Session

from pyccounting.database import (
    Operation,
    anonymous_mode_widget,
    engine,
    get_operation_df,
    reset_widget,
    time_span_widget,
)

anonymous_mode_widget()
time_span_widget()

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

    df_operation: pd.DataFrame = get_operation_df()
    df_operation = df_operation.loc[df_operation["account"] == account]
    if df_operation.empty:
        id_: int = 1
        with open("data/initial_amounts.json") as file:
            amount: float = json.load(file)[account]["amount"]
    else:
        series_latest_operation: pd.Series = df_operation.iloc[-1]
        id_ = series_latest_operation["id_"] + 1
        amount = series_latest_operation["final_amount"]

    with Session(engine) as session:
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

            final_amount = round(amount + operation_amount, 2)
            operation = Operation(
                id_=id_,
                account=account,
                type_=type_,
                label=label,
                date=date,
                initial_amount=amount,
                operation_amount=operation_amount,
                final_amount=final_amount,
            )
            session.add(operation)
            id_ += 1
            amount = final_amount

        session.commit()

reset_widget()
