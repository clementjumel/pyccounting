import pandas as pd
import streamlit as st

from pyccounting import db


def accounts_widget() -> list[str]:
    with st.sidebar:
        df = pd.read_sql(sql="operation", con=db.engine)
        all_accounts = sorted(set(df["account"].values)) + ["total"]

        st.write("Select your account(s):")
        accounts = [account for account in all_accounts if st.checkbox(account, value=True)]
        st.write("---")
        return accounts
