import pandas as pd
import streamlit as st


def table(df: pd.DataFrame, accounts: list[str], anonymous_mode: bool) -> None:
    columns = ["account", "label", "type_"]
    if not anonymous_mode:
        columns = ["initial_amount", "operation_amount", "final_amount"] + columns

    st.dataframe(df[columns].loc[df["account"].isin(accounts)])
