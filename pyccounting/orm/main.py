import datetime
import json

from pyccounting._path import _ROOT
from pyccounting.orm.operations import get_operation_df


def get_start_amount(accounts: list[str], start_date: datetime.date) -> float:
    start_amount: float = 0.0
    with open(_ROOT / "data" / "start_amounts.json") as file:
        d = json.load(file)
        for account in accounts:
            start_amount += d[account]["amount"]

    df = get_operation_df(end_date=start_date, accounts=accounts)
    start_amount += sum(df["amount"])

    return start_amount
