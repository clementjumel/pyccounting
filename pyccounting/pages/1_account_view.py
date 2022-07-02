import datetime

import pandas as pd
import streamlit as st

from pyccounting import db, display, widgets

anonymous_mode: bool = widgets.anonymous_mode()
dates: tuple[datetime.date, datetime.date] = widgets.dates()
accounts: list[str] = widgets.accounts()
widgets.reset()

df: pd.DataFrame = db.get_df(sort_by_date=True, dates=dates)

if df.empty:
    st.write("There's nothing to see, here! ;)")

else:
    display.plot(df=df, dates=dates, accounts=accounts, anonymous_mode=anonymous_mode)
    st.write("---")

    display.statistics(df=df, dates=dates, accounts=accounts, anonymous_mode=anonymous_mode)
    st.write("---")

    display.table(df=df, accounts=accounts, anonymous_mode=anonymous_mode)
