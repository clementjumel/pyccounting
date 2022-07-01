import pandas as pd
import streamlit as st

from pyccounting.database import (
    TimeSpan,
    accounts_widget,
    anonymous_mode_widget,
    get_operation_df,
    reset_widget,
    time_span_widget,
)
from pyccounting.plot import plot
from pyccounting.statistics import statistics
from pyccounting.table import table

anonymous_mode: bool = anonymous_mode_widget()
accounts: list[str] = accounts_widget()
time_span: TimeSpan = time_span_widget()
reset_widget()

st.write("Welcome in Pyccounting.")
st.write("---")

df: pd.DataFrame = get_operation_df(time_span=time_span)

if df.empty:
    st.write("There's nothing to see, here! ;)")

else:
    plot(df=df, accounts=accounts, anonymous_mode=anonymous_mode)
    st.write("---")

    statistics(df=df, accounts=accounts, anonymous_mode=anonymous_mode)
    st.write("---")

    table(df=df, accounts=accounts, anonymous_mode=anonymous_mode)
