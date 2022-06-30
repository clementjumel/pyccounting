import pandas as pd
import streamlit as st

from pyccounting.database import (
    TimeSpan,
    anonymous_mode_widget,
    get_operation_df,
    reset_widget,
    time_span_widget,
)

anonymous_mode: bool = anonymous_mode_widget()
time_span: TimeSpan = time_span_widget()

df: pd.DataFrame = get_operation_df(time_span=time_span)
if anonymous_mode:
    columns = ["account", "label", "type_"]
else:
    columns = ["initial_amount", "operation_amount", "final_amount", "account", "label", "type_"]
    for column in ["initial_amount", "operation_amount", "final_amount"]:
        df[column] = df[column].apply(lambda x: str(round(x, 2)))
df = df[columns]
st.dataframe(df)

reset_widget()
