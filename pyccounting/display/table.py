import pandas as pd
import streamlit as st


def table(df: pd.DataFrame, anonymous_mode: bool) -> None:
    columns = ["account", "label", "type_"]
    if not anonymous_mode:
        columns = ["start_amount", "operation_amount", "end_amount"] + columns

    st.dataframe(df[columns])