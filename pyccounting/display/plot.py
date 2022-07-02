import datetime

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


def _plot_account(ax: plt.Axes, df: pd.DataFrame, account: str, anonymous_mode: bool) -> None:
    df_account = df.loc[df["account"] == account]
    start_date: datetime.date = min(df.index.values)
    end_date: datetime.date = max(df.index.values)
    start_amount: float = df_account.iloc[0]["start_amount"]
    end_amount: float = df_account.iloc[-1]["end_amount"]

    x, y = [start_date], [start_amount]
    for date, row in df_account.iterrows():
        x.append(date)
        y.append(row["end_amount"])
    x.append(end_date)
    y.append(end_amount)

    if not anonymous_mode:
        ax.annotate(
            text=round(start_amount, 2),
            xy=(start_date, start_amount),
            xytext=(-50, 0),
            textcoords="offset points",
        )
        ax.annotate(
            text=round(end_amount, 2),
            xy=(end_date, end_amount),
            xytext=(5, 0),
            textcoords="offset points",
        )
    ax.plot(x, y, label=account)


def _plot_total(ax: plt.Axes, df: pd.DataFrame, accounts: list[str], anonymous_mode: bool) -> None:
    start_date: datetime.date = df.index[0]
    end_date: datetime.date = df.index[-1]

    start_amount: float = 0.0
    for account in accounts:
        if account != "total":
            df_account = df.loc[df["account"] == account]
            start_amount += df_account.iloc[0]["start_amount"]

    amount: float = start_amount
    x, y = [start_date], [start_amount]
    for date, row in df.iterrows():
        amount += row["operation_amount"]
        x.append(date)
        y.append(amount)
    end_amount = y[-1]

    if not anonymous_mode:
        ax.annotate(
            text=round(start_amount, 2),
            xy=(start_date, start_amount),
            xytext=(-50, 0),
            textcoords="offset points",
        )
        ax.annotate(
            text=round(end_amount, 2),
            xy=(end_date, end_amount),
            xytext=(5, 0),
            textcoords="offset points",
        )
    ax.plot(x, y, label="total")


def plot(df: pd.DataFrame, accounts: list[str], anonymous_mode: bool) -> None:
    fig, ax = plt.subplots()
    for account in accounts:
        if account != "total":
            _plot_account(ax=ax, df=df, account=account, anonymous_mode=anonymous_mode)
        else:
            _plot_total(ax=ax, df=df, accounts=accounts, anonymous_mode=anonymous_mode)

    if not anonymous_mode:
        ax.axhline(y=0, color="k")
    ax.grid(True, which="both")
    ax.set_yticklabels([])
    plt.xlim(min(df.index.values), max(df.index.values))
    plt.legend()
    st.pyplot(fig=fig)
