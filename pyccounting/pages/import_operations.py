from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st
from sqlalchemy.orm import Session

from pyccounting.database import Operation, engine

account = st.selectbox("Account", ("bnp", "fortuneo"))
uploaded_file = st.file_uploader(label="Upload a file", type=["csv", "xls"])
if uploaded_file is not None:

    sep = "," if account == "bnp" else ";"
    df = pd.read_csv(uploaded_file, sep=sep)
    st.dataframe(df)

    with Session(engine) as session:
        ids = [t[0] for t in session.query(Operation.id_).all()]
        offset = max(ids) + 1 if ids else 0
        for i, row in df.iterrows():

            if account == "bnp":
                operation = Operation(
                    id_=i + offset,
                    account=account,
                    type_=row["Type operation"],
                    label=row["Libelle operation"],
                    date=datetime.strptime(row["Date operation"], "%d/%m/%Y").date(),
                    amount=float(row["Montant operation en euro"].replace(",", ".")),
                )

            else:
                if row["Débit"] and row["Crédit"] is np.nan:
                    amount_column = "Débit"
                elif row["Crédit"] and row["Débit"] is np.nan:
                    amount_column = "Crédit"
                else:
                    raise ValueError()
                operation = Operation(
                    id_=i + offset,
                    account=account,
                    type_="unknown",
                    label=row["libellé"],
                    date=datetime.strptime(row["Date opération"], "%d/%m/%Y").date(),
                    amount=float(row[amount_column].replace(",", ".")),
                )

            session.add(operation)
        session.commit()
