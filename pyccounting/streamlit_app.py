import json

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from pyccounting.database import get_operation_df
from pyccounting.plot import plot_account

st.write("Welcome in Pyccounting.")

df: pd.DataFrame = get_operation_df()
df = df[["account", "amount"]]

dates = df.index.values
min_date, max_date = min(dates), max(dates)

accounts: list[str] = sorted(set(df["account"].values))
display_accounts = [account for account in accounts if st.checkbox(account, value=True)]
display_total = st.checkbox("total", value=True)

with open("data/start.json") as file:
    start_amounts = json.load(file)

fig, ax = plt.subplots()
for account in display_accounts:
    plot_account(
        ax=ax,
        account=account,
        start_amount=start_amounts[account]["amount"],
        series_account=df.loc[df["account"] == account]["amount"],
        min_date=min_date,
        max_date=max_date,
    )
if display_total:
    plot_account(
        ax=ax,
        account="total",
        start_amount=sum(start_amounts[account]["amount"] for account in accounts),
        series_account=df["amount"],
        min_date=min_date,
        max_date=max_date,
    )

ax.axhline(y=0, color="k")
ax.grid(True, which="both")
ax.set_yticklabels([])
plt.xlim(min_date, max_date)
plt.legend()
st.pyplot(fig=fig)
