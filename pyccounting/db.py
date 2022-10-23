from __future__ import annotations

import datetime
import json

import pandas as pd
import streamlit as st
from sqlalchemy import Boolean, Column, Date, Float, Integer, String, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base

engine: Engine = create_engine(url="sqlite:///data/db/sqlite.db")

Base = declarative_base()


class Operation(Base):  # type: ignore
    __tablename__ = "operation"

    id_ = Column(Integer, primary_key=True, index=True)
    account = Column(String, primary_key=True, index=True)
    label = Column(String)
    date = Column(Date)
    amount = Column(Float)
    category = Column(String)
    validated = Column(Boolean)

    def to_string(self, anonymous_mode: bool) -> str:
        attrs = ["date", "label", "account", "category"]
        if not anonymous_mode:
            attrs = ["amount"] + attrs
        return ", ".join([getattr(self, attr) for attr in attrs])

    def set_validated(self, anonymous_mode: bool) -> None:
        self.validated = True
        text = self.to_string(anonymous_mode=anonymous_mode)
        st.write(f"Validation of operation '{text}'.")

    def set_category(self, category: str, anonymous_mode: bool) -> None:
        self.category = category
        text = self.to_string(anonymous_mode=anonymous_mode)
        st.write(f"Category '{category}' set for operation '{text}'.")

    def apply_category_rules(
        self,
        category_rules: list[CategoryRule],
        anonymous_mode: bool,
    ) -> None:
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
                self.set_category(
                    category=category_rule.category,
                    anonymous_mode=anonymous_mode,
                )
                return


class CategoryRule(Base):  # type: ignore
    __tablename__ = "category_rule"

    category = Column(String, primary_key=True, index=True)
    content = Column(String, primary_key=True, index=True)


def get_df(
    accounts: list[str] | None = None,
    types: list[str] | None = None,
    categories: list[str] | None = None,
    date_index: bool = True,
    sort_by_date: bool = False,
    dates: tuple[datetime.date, datetime.date] | None = None,
    validated_status: bool | None = None,
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

    if validated_status is not None:
        df = df.loc[df["validated"] == validated_status]

    df["date"] = df["date"].apply(lambda x: x.date())
    if date_index:
        df = df.set_index("date")

    if sort_by_date:
        df = df.sort_values(by="date")

    if dates is not None:
        df = df.loc[dates[0] : dates[1]]  # type: ignore

    return df


def get_start_amount(accounts: list[str], date: datetime.date) -> float:
    start_amount: float = 0.0
    with open("data/start_amounts.json") as file:
        d = json.load(file)
        for account in accounts:
            start_amount += d[account]["amount"]

    df = get_df(accounts=accounts, sort_by_date=True)
    df = df.loc[:date]  # type: ignore
    start_amount += sum(df["amount"])

    return start_amount
