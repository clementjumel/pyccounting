import pandas as pd
import streamlit as st

from pyccounting.database import get_operation_df

df: pd.DataFrame = get_operation_df()
df = df[["account", "amount", "label", "type_"]]

st.dataframe(df)
