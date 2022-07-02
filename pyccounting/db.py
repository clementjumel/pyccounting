from __future__ import annotations

import datetime
import os

import pandas as pd
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
    start_amount = Column(Float)
    operation_amount = Column(Float)
    end_amount = Column(Float)


os.makedirs("data/db/", exist_ok=True)
with Session(engine) as session:
    Base.metadata.create_all(bind=session.bind)


def get_operation_df(time_span: str = "All") -> pd.DataFrame:
    df = pd.read_sql(sql="operation", con=engine)

    df["date"] = df["date"].apply(lambda x: x.date())
    df = df.sort_values(by="date")
    df = df.set_index("date")

    if time_span == "All":
        pass
    else:
        if time_span == "Last year":
            days = 365
        elif time_span == "Last quarter":
            days = 93
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
