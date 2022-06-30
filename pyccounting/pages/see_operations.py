import pandas as pd
import streamlit as st

from pyccounting.database import TimeSpan, get_operation_df, reset_widget, time_span_widget

time_span: TimeSpan = time_span_widget()

df: pd.DataFrame = get_operation_df(time_span=time_span)
df = df[["initial_amount", "operation_amount", "final_amount", "account", "label", "type_"]]
st.dataframe(df)

reset_widget()
