import datetime

import pandas as pd
import streamlit as st

from pyccounting import db, display, initialize, widgets

initialize.initialize()

dates: tuple[datetime.date, datetime.date] = widgets.dates()
accounts: list[str] = widgets.accounts(extended=True)
types: list[str] = widgets.types(extended=True)
anonymous_mode: bool = widgets.anonymous_mode()
widgets.reset()

df: pd.DataFrame = db.get_df(
    accounts=accounts,
    types=types,
    sort_by_date=True,
    dates=dates,
)

if df.empty:
    st.write("There's nothing to see here! 😇")

else:
    display.plot(
        df=df,
        dates=dates,
        accounts=accounts,
        types=types,
        anonymous_mode=anonymous_mode,
    )
    st.write("---")

    display.pie_chart(df=df, types=types)
    st.write("---")

    display.statistics(
        df=df,
        dates=dates,
        accounts=accounts,
        types=types,
        anonymous_mode=anonymous_mode,
    )
