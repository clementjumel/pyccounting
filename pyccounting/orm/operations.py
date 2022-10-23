import datetime

import pandas as pd
import streamlit as st
from sqlalchemy.orm import Session

from .categories import get_default_category_id
from .data_model import Operation, Rule
from .db import engine
from .rules import get_rules


def get_operation_idx() -> int:
    with Session(engine) as session:
        operations: list[Operation] = session.query(Operation).order_by(Operation.idx).all()

    if operations:
        return operations[-1].idx + 1
    return 0


def add_operation_df(df: pd.DataFrame, account: str, verbose: bool = False) -> None:
    rules: list[Rule] = get_rules()
    default_category_id: str = get_default_category_id()
    idx: int = get_operation_idx()

    with Session(engine) as session:
        operations: list[Operation] = []
        for _, row in df.iterrows():
            operation = Operation.from_row(row=row, account=account, idx=idx)
            operation.find_category(rules=rules, default_category_id=default_category_id)
            operations.append(operation)
            idx += 1
        session.add_all(operations)
        session.commit()

    if verbose:
        st.info(f"{len(operations)} operations added.")


def get_operation_df(
    accounts: list[str] | None = None,
    types: list[str] | None = None,
    category_names: list[str] | None = None,
    date_index: bool = False,
    sort_by_date: bool = False,
    dates: tuple[datetime.date, datetime.date] | None = None,
) -> pd.DataFrame:
    with Session(engine) as session:
        operations: list[Operation] = session.query(Operation).order_by(Operation.idx).all()
        records: list[dict] = [operation.to_dict() for operation in operations]
        df: pd.DataFrame = pd.DataFrame.from_records(records)

    if accounts is not None:
        df = df.loc[df["account"].isin(accounts)]

    if types is not None:
        if types == ["expenses"]:
            df = df.loc[df["amount"] < 0]
        elif types == ["incomes"]:
            df = df.loc[df["amount"] >= 0]
        elif not types:
            df = df.loc[[False for _ in df.index]]

    if category_names is not None:
        df = df.loc[df["category_name"].isin(category_names)]

    if date_index:
        df = df.set_index("date")
    else:
        df = df.set_index("idx")

    if sort_by_date:
        df = df.sort_values(by="date")

    if dates is not None:
        df = df.loc[dates[0] : dates[1]]  # type: ignore

    return df
