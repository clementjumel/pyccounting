import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from pyccounting.database import TimeSpan, get_operation_df, reset_widget, time_span_widget
from pyccounting.plot import plot_account, plot_total

time_span: TimeSpan = time_span_widget()

st.write("Welcome in Pyccounting.")

df: pd.DataFrame = get_operation_df(time_span=time_span)

if df.empty:
    st.write("There's nothing to see, here! ;)")
else:
    dates = df.index.values
    initial_date, final_date = min(dates), max(dates)

    accounts: list[str] = sorted(set(df["account"].values))
    display_accounts = [account for account in accounts if st.checkbox(account, value=True)]
    display_total = st.checkbox("total", value=True)

    fig, ax = plt.subplots()
    for account in display_accounts:
        plot_account(
            ax=ax,
            df=df,
            account=account,
            initial_date=initial_date,
            final_date=final_date,
        )

    if display_total:
        plot_total(
            ax=ax,
            df=df,
            accounts=accounts,
        )

    ax.axhline(y=0, color="k")
    ax.grid(True, which="both")
    ax.set_yticklabels([])
    plt.xlim(initial_date, final_date)
    plt.legend()
    st.pyplot(fig=fig)

reset_widget()
