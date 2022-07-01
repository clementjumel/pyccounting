from __future__ import annotations

import datetime
import os
from typing import Literal

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import Column, Date, Float, Integer, String, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, declarative_base

load_dotenv()
engine: Engine = create_engine(url=f"sqlite:///data/db/{os.getenv('DB_NAME')}")

Base = declarative_base()


class Operation(Base):  # type: ignore
    __tablename__ = "operation"

    id_ = Column(Integer, primary_key=True, index=True)
    account = Column(String, primary_key=True, index=True)
    type_ = Column(String)
    label = Column(String)
    date = Column(Date)
    initial_amount = Column(Float)
    operation_amount = Column(Float)
    final_amount = Column(Float)


os.makedirs("data/db/", exist_ok=True)
with Session(engine) as session:
    Base.metadata.create_all(bind=session.bind)


def anonymous_mode_widget() -> bool:
    if os.getenv("ANONYMOUS_MODE") == "1":
        with st.sidebar:
            anonymous_mode = st.checkbox("Anonymous mode", value=True)
            st.write("---")
            return anonymous_mode

    return False


def reset_widget() -> None:
    if os.getenv("RESET_BUTTON") == "1":
        with st.sidebar:
            reset = st.button("Reset")
            st.write("---")
            if reset:
                with Session(engine) as session:
                    Base.metadata.drop_all(bind=session.bind)
                    Base.metadata.create_all(bind=session.bind)


TimeSpan = Literal["All", "Last year", "Last month", "Last week"]
TIME_SPAN_VALUES = TimeSpan.__args__  # type: ignore


def time_span_widget() -> TimeSpan:
    with st.sidebar:
        time_span = st.radio("Select a time span", TIME_SPAN_VALUES)
        st.write("---")
        return time_span


def get_operation_df(time_span: TimeSpan = TIME_SPAN_VALUES[0]) -> pd.DataFrame:
    df = pd.read_sql(sql="operation", con=engine)

    df["date"] = df["date"].apply(lambda x: x.date())
    df = df.sort_values(by="date")
    df = df.set_index("date")

    if time_span == "All":
        pass
    else:
        if time_span == "Last year":
            days = 365
        elif time_span == "Last month":
            days = 31
        elif time_span == "Last week":
            days = 7
        else:
            raise ValueError
        min_datetime = datetime.datetime.now() - datetime.timedelta(days=days)
        min_date = min_datetime.date()
        df = df.loc[min_date:]  # type: ignore

    return df
