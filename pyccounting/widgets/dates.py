import datetime

import streamlit as st

from pyccounting import db


def dates_widget() -> tuple[datetime.date, datetime.date]:
    df = db.get_df(sort_by_date=True)
    with st.sidebar:
        dates = st.date_input(
            "Select a starting date or a date range:",
            value=(min(df.index), max(df.index)),
        )
        st.write("---")

        if len(dates) == 2:
            return dates
        elif len(dates) == 1:
            return dates[0], datetime.date.today()
        else:
            raise ValueError