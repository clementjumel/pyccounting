import pandas as pd
import streamlit as st


def table(df: pd.DataFrame, anonymous_mode: bool) -> None:
    columns = ["account", "label", "category"]
    if not anonymous_mode:
        columns = ["amount"] + columns

    st.dataframe(df[columns])
