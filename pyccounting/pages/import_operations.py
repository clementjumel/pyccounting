import pandas as pd
import streamlit as st

uploaded_file = st.file_uploader(label="Upload a file", type=["csv", "xls"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    if list(df.columns) == [
        "Date operation",
        "Libelle court",
        "Type operation",
        "Libelle operation",
        "Montant operation en euro",
    ]:
        format_ = "bnp"
    elif list(df.columns) == [
        "Date opération",
        "Date valeur",
        "libellé",
        "Débit",
        "Crédit",
    ]:
        format_ = "fortuneo"
    else:
        raise ValueError

    # TODO
    # from sqlalchemy.orm import Session
    # from pyccounting.database import Operation, engine
    # with Session(engine) as session:
    #     for _, row in df.iterrows():
    #         operation = Operation.from_row(row, format_=format_)
    #         session.add(operation)
    #
    #     session.commit()
