import streamlit as st


def accounts_widget(extended: bool = False) -> list[str]:
    with st.sidebar:
        options = ["bnp", "fortuneo"]
        if extended:
            options.append("total")

        st.write("Select your account(s):")
        accounts = [account for account in options if st.checkbox(account, value=True)]
        st.write("---")
        return accounts
