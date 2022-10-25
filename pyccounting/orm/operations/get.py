import datetime

import pandas as pd
from sqlalchemy.orm import Query, Session

from pyccounting.orm.categories import get_category
from pyccounting.orm.data_model import Category, Operation
from pyccounting.orm.database import engine


def get_operations(order_by_date: bool = False) -> list[Operation]:
    with Session(engine) as session:
        query: Query = session.query(Operation)
        if order_by_date:
            query = query.order_by(Operation.date)
        else:
            query = query.order_by(Operation.idx)
        return query.all()


def get_category_operations(category_name: str) -> list[Operation]:
    category: Category = get_category(category_name=category_name)
    with Session(engine) as session:
        return (
            session.query(Operation)
            .filter(Operation.category_id == category.id_)
            .order_by(Operation.idx)
            .all()
        )


def get_rule_operations(rule_id: str) -> list[Operation]:
    with Session(engine) as session:
        return (
            session.query(Operation)
            .filter(Operation.rule_id == rule_id)
            .order_by(Operation.idx)
            .all()
        )


def get_operation_idx() -> int:
    operations: list[Operation] = get_operations()
    if operations:
        return operations[-1].idx + 1
    return 0


def get_operation_df(
    start_date: datetime.date = None,
    end_date: datetime.date = None,
    accounts: list[str] = None,
    types: list[str] = None,
    category_names: list[str] = None,
    date_index: bool = False,
    sort_by_date: bool = False,
) -> pd.DataFrame:
    with Session(engine) as session:
        operations: list[Operation] = session.query(Operation).order_by(Operation.idx).all()
        records: list[dict] = [operation.to_dict() for operation in operations]
        df: pd.DataFrame = pd.DataFrame.from_records(records)

    if df.empty:
        return df

    if start_date is not None:
        df = df.loc[df["date"] >= start_date]

    if end_date is not None:
        df = df.loc[df["date"] <= end_date]

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

    return df
