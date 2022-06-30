import numpy as np
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

statistics = [
    ("Minimum operation amount", min(df["operation_amount"])),
    ("Maximum operation amount", max(df["operation_amount"])),
    ("Average operation amount", round(float(np.mean(df["operation_amount"])), 2)),
    ("Total operation amount", round(sum(df["operation_amount"]), 2)),
]

for name, result in statistics:
    text = f"{name}: XXX" if anonymous_mode else f"{name}: {result}"
    st.write(text)

reset_widget()
