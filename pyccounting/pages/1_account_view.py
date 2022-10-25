import datetime

import pandas as pd
import streamlit as st

from pyccounting import display, initialize, orm, widgets

initialize.initialize()

start_date: datetime.date = widgets.start_date()
accounts: list[str] = widgets.accounts(extended=True)
types: list[str] = widgets.types(extended=True)
category_names: list[str] = widgets.categories()

operation_df: pd.DataFrame = orm.get_operation_df(
    start_date=start_date,
    accounts=accounts,
    types=types,
    category_names=category_names,
    date_index=True,
    sort_by_date=True,
)

st.title("Welcome in Pyccounting 😎")
st.write(
    f"There are **{len(orm.get_operations())} operations** in total, "
    f"and **{len(operation_df)} operations** selected."
)

if operation_df.empty:
    st.error("There's no operation selected.")

else:
    display.plot(
        df=operation_df,
        start_date=start_date,
        accounts=accounts,
        types=types,
    )
    st.write("---")

    display.pie_chart(
        df=operation_df,
        types=types,
    )
    st.write("---")

    display.statistics(
        df=operation_df,
        start_date=start_date,
        accounts=accounts,
        types=types,
    )
