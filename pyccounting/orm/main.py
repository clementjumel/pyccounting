import datetime
import json

import pandas as pd

from pyccounting import _ROOT

from .db import engine


def get_df(
    accounts: list[str] | None = None,
    types: list[str] | None = None,
    category_names: list[str] | None = None,
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

    if category_names is not None:
        df = df.loc[df["category_name"].isin(category_names)]

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
    with open(_ROOT / "data" / "start_amounts.json") as file:
        d = json.load(file)
        for account in accounts:
            start_amount += d[account]["amount"]

    df = get_df(accounts=accounts, sort_by_date=True)
    df = df.loc[:date]  # type: ignore
    start_amount += sum(df["amount"])

    return start_amount
