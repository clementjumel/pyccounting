import datetime

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


def plot(
    df: pd.DataFrame,
    dates: tuple[datetime.date, datetime.date],
    accounts: list[str],
    anonymous_mode: bool,
) -> None:
    fig, ax = plt.subplots()

    for account in accounts:
        df_account = df.loc[df["account"] == account]
        start_amount: float = df_account.iloc[0]["start_amount"]
        end_amount: float = df_account.iloc[-1]["end_amount"]

        x, y = [dates[0]], [start_amount]
        for date, row in df_account.iterrows():
            x.append(date)
            y.append(row["end_amount"])
        x.append(dates[1])
        y.append(end_amount)

        if not anonymous_mode:
            ax.annotate(
                text=round(start_amount, 2),
                xy=(dates[0], start_amount),
                xytext=(-50, 0),
                textcoords="offset points",
            )
            ax.annotate(
                text=round(end_amount, 2),
                xy=(dates[1], end_amount),
                xytext=(5, 0),
                textcoords="offset points",
            )
        ax.plot(x, y, label=account)

    if len(accounts) > 1:
        start_amount = 0.0
        for account in accounts:
            if account != "total":
                df_account = df.loc[df["account"] == account]
                start_amount += df_account.iloc[0]["start_amount"]

        amount: float = start_amount
        x, y = [dates[0]], [start_amount]
        for date, row in df.iterrows():
            amount += row["operation_amount"]
            x.append(date)
            y.append(amount)
        end_amount = y[-1]
        x.append(dates[1])
        y.append(end_amount)

        if not anonymous_mode:
            ax.annotate(
                text=round(start_amount, 2),
                xy=(dates[0], start_amount),
                xytext=(-50, 0),
                textcoords="offset points",
            )
            ax.annotate(
                text=round(end_amount, 2),
                xy=(dates[1], end_amount),
                xytext=(5, 0),
                textcoords="offset points",
            )
        ax.plot(x, y, label="total")

    if not anonymous_mode:
        ax.axhline(y=0, color="k")
    ax.grid(True, which="both")
    ax.set_yticklabels([])
    plt.xlim(dates[0], dates[1])
    plt.yticks(range(-10000, 80001, 10000))
    plt.legend()
    st.pyplot(fig=fig)
