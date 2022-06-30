import datetime

import pandas as pd


def plot_account(
    ax,
    account: str,
    start_amount: float,
    series_account: pd.Series,
    min_date: datetime.date,
    max_date: datetime.date,
) -> None:
    total_amount: float = start_amount
    x, y = [min_date], [start_amount]
    for date, operation_amount in series_account.items():
        total_amount += operation_amount
        x.append(date)
        y.append(total_amount)
    x.append(max_date)
    y.append(total_amount)

    ax.annotate(
        text=round(y[0], 2),
        xy=(min_date, y[0]),
        xytext=(-50, 0),
        textcoords="offset points",
    )
    ax.annotate(
        text=round(y[-1], 2),
        xy=(max_date, y[-1]),
        xytext=(5, 0),
        textcoords="offset points",
    )
    ax.plot(x, y, label=account)
