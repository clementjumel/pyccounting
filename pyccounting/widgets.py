import os

import pandas as pd
import streamlit as st
from sqlalchemy.orm import Session

from pyccounting.database import Base, engine


def reset_widget() -> None:
    if os.getenv("RESET_BUTTON") == "1":
        with st.sidebar:
            reset = st.button("Reset")
            st.write("---")
            if reset:
                with Session(engine) as session:
                    Base.metadata.drop_all(bind=session.bind)
                    Base.metadata.create_all(bind=session.bind)


def anonymous_mode_widget() -> bool:
    if os.getenv("ANONYMOUS_MODE") == "1":
        with st.sidebar:
            anonymous_mode = st.checkbox("Anonymous mode", value=True)
            st.write("---")
            return anonymous_mode

    return False


def time_span_widget() -> str:
    with st.sidebar:
        time_span = st.radio(
            "Select a time span",
            ["All", "Last year", "Last quarter", "Last month", "Last week"],
        )
        st.write("---")
        return time_span


def accounts_widget() -> list[str]:
    with st.sidebar:
        df = pd.read_sql(sql="operation", con=engine)
        all_accounts = sorted(set(df["account"].values)) + ["total"]

        st.write("Select your account(s):")
        accounts = [account for account in all_accounts if st.checkbox(account, value=True)]
        st.write("---")
        return accounts
