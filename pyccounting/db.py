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


def get_df(
    sort_by_date: bool = False,
    dates: tuple[datetime.date] | tuple[datetime.date, datetime.date] | None = None,
) -> pd.DataFrame:
    df = pd.read_sql(sql="operation", con=engine)
    df["date"] = df["date"].apply(lambda x: x.date())
    df = df.set_index("date")

    if sort_by_date:
        df = df.sort_values(by="date")

    if dates:
        if len(dates) == 1:
            df = df.loc[dates[0] :]  # type: ignore
        elif len(dates) == 2:
            df = df.loc[dates[0] : dates[1]]  # type: ignore
        else:
            raise ValueError

    return df
