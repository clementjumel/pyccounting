from __future__ import annotations

import datetime
import os

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
    label = Column(String)
    date = Column(Date)
    amount = Column(Float)
    category = Column(String)

    def apply_category_rules(self, category_rules: list[CategoryRule]) -> None:
        if self.category != "":
            return

        target_tokens = [token.upper() for token in self.label.strip().split()]
        target = " ".join(target_tokens)
        for category_rule in category_rules:
            content_tokens = [token.upper() for token in category_rule.content.strip().split()]
            content = " ".join(content_tokens)

            match = False
            if len(content_tokens) == 1 and content_tokens[0] in target_tokens:
                match = True
            elif len(content_tokens) > 1 and content in target:
                match = True

            if match:
                self.category = category_rule.category
                st.write(f"Category found for '{self.label}': {self.category}.")
                return


class CategoryRule(Base):  # type: ignore
    __tablename__ = "category_rule"

    category = Column(String, primary_key=True, index=True)
    content = Column(String, primary_key=True, index=True)


os.makedirs("data/db/", exist_ok=True)
with Session(engine) as session:
    Base.metadata.create_all(bind=session.bind)


def get_df(
    accounts: list[str] | None = None,
    types: list[str] | None = None,
    categories: list[str] | None = None,
    date_index: bool = True,
    sort_by_date: bool = False,
    dates: tuple[datetime.date, datetime.date] | None = None,
) -> pd.DataFrame:
    df = pd.read_sql(sql="operation", con=engine)

    if accounts is not None:
        df = df.loc[df["account"].isin(accounts)]

    if types is not None:
        if types == ["expenses"]:
            df = df.loc[df["amount"] < 0]
        elif types == ["incomes"]:
            df = df.loc[df["amount"] >= 0]
        elif not types:
            df = df.loc[[False for _ in df.index]]

    if categories is not None:
        df = df.loc[df["category"].isin(categories)]

    df["date"] = df["date"].apply(lambda x: x.date())
    if date_index:
        df = df.set_index("date")

    if sort_by_date:
        df = df.sort_values(by="date")

    if dates is not None:
        df = df.loc[dates[0] : dates[1]]  # type: ignore

    return df
