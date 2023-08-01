import datetime

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from pyccounting import orm

COLORS = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
]


def _plot_line(
    ax: plt.Axes,
    df: pd.DataFrame,
    start_date: datetime.date,
    start_amount: float,
    annotate: bool,
    kwargs: dict,
) -> None:
    x: list[datetime.date] = [start_date]
    y: list[float] = [start_amount]

    amount: float = start_amount
    for date, row in df.iterrows():
        amount += row["amount"]
        x.append(date)
        y.append(amount)

    x.append(datetime.date.today())
    y.append(y[-1])

    if annotate:
        ax.annotate(
            text=round(y[0], 2),
            xy=(start_date, y[0]),
            xytext=(-50, 0),
            textcoords="offset points",
        )
        ax.annotate(
            text=round(y[-1], 2),
            xy=(datetime.date.today(), y[-1]),
            xytext=(5, 0),
            textcoords="offset points",
        )

    ax.plot(x, y, **kwargs)


def plot(
    df: pd.DataFrame,
    start_date: datetime.date,
    accounts: list[str],
    types: list[str],
) -> None:
    fig, ax = plt.subplots()

    for i, account in enumerate(accounts):
        color = COLORS[i]
        start_amount = orm.get_start_amount(
            accounts=(
                [account]
                if account != "total"
                else [account_ for account_ in accounts if account_ != "total"]
            ),
            start_date=start_date,
        )

        for type_ in types:
            df_ = df.loc[df["account"] == account] if account != "total" else df
            if type_ == "expenses":
                df_ = df_.loc[df_["amount"] < 0]
            elif type_ == "incomes":
                df_ = df_.loc[df_["amount"] >= 0]
            elif type_ == "expenses & incomes":
                pass
            else:
                raise ValueError

            kwargs: dict = {"color": color}
            annotate = True
            if type_ == "expenses & incomes" or "expenses & incomes" not in types:
                kwargs["label"] = account
            if type_ != "expenses & incomes":
                kwargs["linestyle"] = "dashed"
                kwargs["linewidth"] = 0.6
                kwargs["marker"] = "o"
                kwargs["markersize"] = 0.6
                annotate = False

            _plot_line(
                ax=ax,
                df=df_,
                start_date=start_date,
                start_amount=start_amount,
                annotate=annotate,
                kwargs=kwargs,
            )

    st.write("### Evolution")

    ax.axhline(y=0, color="k")
    ax.grid(True, which="both")
    ax.set_yticklabels([])
    plt.xlim(start_date, datetime.date.today())
    plt.yticks(range(-30000, 100001, 10000))
    plt.legend()
    st.pyplot(fig=fig)
