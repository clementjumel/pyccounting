import pandas as pd
import streamlit as st

from pyccounting.database import TimeSpan, get_operation_df, reset_widget, time_span_widget

time_span: TimeSpan = time_span_widget()

df: pd.DataFrame = get_operation_df()
df = df[["account", "amount", "label", "type_"]]
st.dataframe(df)

reset_widget()
