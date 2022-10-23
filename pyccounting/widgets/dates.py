import datetime

import streamlit as st

from pyccounting import orm


def dates_widget() -> tuple[datetime.date, datetime.date]:
    with st.sidebar:
        df = orm.get_operation_df(date_index=True, sort_by_date=True)
        if not df.empty:
            value = (min(df.index), max(df.index))
        else:
            value = (datetime.date.today(), datetime.date.today())

        dates = st.date_input("Select a starting date or a date range:", value=value)
        st.write("---")

        if len(dates) == 2:
            return dates
        elif len(dates) == 1:
            return dates[0], datetime.date.today()
        else:
            raise ValueError
