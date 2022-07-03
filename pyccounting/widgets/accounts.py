import streamlit as st

from pyccounting import db


def accounts_widget(extended: bool = False) -> list[str]:
    with st.sidebar:
        df = db.get_df()
        options = sorted(set(df["account"].values))
        if extended:
            options.append("total")

        st.write("Select your account(s):")
        accounts = [account for account in options if st.checkbox(account, value=True)]
        st.write("---")
        return accounts
