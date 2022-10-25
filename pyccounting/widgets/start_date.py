import datetime

import orm
import streamlit as st


def start_date_widget() -> datetime.date:
    with st.sidebar:
        time_span: str = st.radio(
            label="Select a time span:",
            options=[
                "ever",
                "last year",
                "last 6 months",
                "last 3 months",
                "last month",
            ],
        )
        st.write("---")

        if time_span == "ever":
            operations: list[orm.Operation] = orm.get_operations(order_by_date=True)
            return operations[0].date

        if time_span == "last year":
            delta: datetime.timedelta = datetime.timedelta(days=365)
        elif time_span == "last 6 months":
            delta = datetime.timedelta(days=180)
        elif time_span == "last 3 months":
            delta = datetime.timedelta(days=90)
        elif time_span == "last month":
            delta = datetime.timedelta(days=30)
        else:
            raise ValueError
        return datetime.date.today() - delta
