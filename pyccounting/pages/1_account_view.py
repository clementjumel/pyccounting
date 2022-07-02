import pandas as pd
import streamlit as st

from pyccounting import db, display, widgets

anonymous_mode: bool = widgets.anonymous_mode()
accounts: list[str] = widgets.accounts()
time_span: str = widgets.time_span()
widgets.reset()

df: pd.DataFrame = db.get_operation_df(time_span=time_span)

if df.empty:
    st.write("There's nothing to see, here! ;)")

else:
    display.plot(df=df, accounts=accounts, anonymous_mode=anonymous_mode)
    st.write("---")

    display.statistics(df=df, accounts=accounts, anonymous_mode=anonymous_mode)
    st.write("---")

    display.table(df=df, accounts=accounts, anonymous_mode=anonymous_mode)
