import datetime

import matplotlib.pyplot as plt
import pandas as pd


def plot_account(
    ax: plt.Axes,
    df: pd.DataFrame,
    account: str,
    initial_date: datetime.date,
    final_date: datetime.date,
) -> None:
    df_account = df.loc[df["account"] == account]
    initial_amount: float = df_account.iloc[0]["initial_amount"]
    final_amount: float = df_account.iloc[-1]["final_amount"]

    x, y = [initial_date], [initial_amount]
    for date, row in df_account.iterrows():
        x.append(date)
        y.append(row["final_amount"])
    x.append(final_date)
    y.append(final_amount)

    ax.annotate(
        text=round(initial_amount, 2),
        xy=(initial_date, initial_amount),
        xytext=(-50, 0),
        textcoords="offset points",
    )
    ax.annotate(
        text=round(final_amount, 2),
        xy=(final_date, final_amount),
        xytext=(5, 0),
        textcoords="offset points",
    )
    ax.plot(x, y, label=account)


def plot_total(
    ax: plt.Axes,
    df: pd.DataFrame,
    accounts: list[str],
) -> None:
    initial_date: datetime.date = df.index[0]
    final_date: datetime.date = df.index[-1]

    initial_amount: float = 0.0
    for account in accounts:
        df_account = df.loc[df["account"] == account]
        initial_amount += df_account.iloc[0]["initial_amount"]

    amount: float = initial_amount
    x, y = [initial_date], [initial_amount]
    for date, row in df.iterrows():
        amount += row["operation_amount"]
        x.append(date)
        y.append(amount)
    final_amount = y[-1]

    ax.annotate(
        text=round(initial_amount, 2),
        xy=(initial_date, initial_amount),
        xytext=(-50, 0),
        textcoords="offset points",
    )
    ax.annotate(
        text=round(final_amount, 2),
        xy=(final_date, final_amount),
        xytext=(5, 0),
        textcoords="offset points",
    )
    ax.plot(x, y, label="total")
