import streamlit as st

from pyccounting import db


def accounts_widget() -> list[str]:
    with st.sidebar:
        df = db.get_df()
        st.write("Select your account(s):")
        accounts = [
            account
            for account in sorted(set(df["account"].values))
            if st.checkbox(account, value=True)
        ]
        st.write("---")
        return accounts
