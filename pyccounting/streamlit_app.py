import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from pyccounting.database import (
    TimeSpan,
    anonymous_mode_widget,
    get_operation_df,
    reset_widget,
    time_span_widget,
)
from pyccounting.plot import plot_account, plot_total

anonymous_mode: bool = anonymous_mode_widget()
time_span: TimeSpan = time_span_widget()
reset_widget()

st.write("Welcome in Pyccounting.")
st.write("---")

df: pd.DataFrame = get_operation_df(time_span=time_span)

if df.empty:
    st.write("There's nothing to see, here! ;)")

else:
    dates = df.index.values
    initial_date, final_date = min(dates), max(dates)

    st.write("Select the account you want to display:")
    accounts: list[str] = sorted(set(df["account"].values))
    display_accounts = [account for account in accounts if st.checkbox(account, value=True)]
    display_total = st.checkbox("total", value=True)

    st.write("")

    fig, ax = plt.subplots()
    for account in display_accounts:
        plot_account(
            ax=ax,
            df=df,
            account=account,
            initial_date=initial_date,
            final_date=final_date,
            anonymous_mode=anonymous_mode,
        )

    if display_total:
        plot_total(
            ax=ax,
            df=df,
            accounts=accounts,
            anonymous_mode=anonymous_mode,
        )

    if not anonymous_mode:
        ax.axhline(y=0, color="k")
    ax.grid(True, which="both")
    ax.set_yticklabels([])
    plt.xlim(initial_date, final_date)
    plt.legend()
    st.pyplot(fig=fig)

    st.write("")

    columns = ["account", "label", "type_"]
    if not anonymous_mode:
        columns.extend(["initial_amount", "operation_amount", "final_amount"])
    st.dataframe(df[columns])

    st.write("")

    statistics = [
        ("Minimum operation amount", min(df["operation_amount"])),
        ("Maximum operation amount", max(df["operation_amount"])),
        ("Average operation amount", round(float(np.mean(df["operation_amount"])), 2)),
        ("Total operation amount", round(sum(df["operation_amount"]), 2)),
    ]

    for name, result in statistics:
        text = f"{name}: XXX" if anonymous_mode else f"{name}: {result}"
        st.write(text)
