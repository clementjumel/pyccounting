import datetime
import json

from pyccounting import _ROOT

from .operations import get_operation_df


def get_start_amount(accounts: list[str], date: datetime.date) -> float:
    start_amount: float = 0.0
    with open(_ROOT / "data" / "start_amounts.json") as file:
        d = json.load(file)
        for account in accounts:
            start_amount += d[account]["amount"]

    df = get_operation_df(accounts=accounts, sort_by_date=True)
    df = df.loc[:date]  # type: ignore
    start_amount += sum(df["amount"])

    return start_amount
