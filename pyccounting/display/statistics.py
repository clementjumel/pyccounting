import datetime

import numpy as np
import pandas as pd
import streamlit as st


def statistics(
    df: pd.DataFrame,
    dates: tuple[datetime.date, datetime.date],
    accounts: list[str],
    anonymous_mode: bool,
) -> None:
    def statistics_account(account: str) -> None:
        df_account = df.loc[df["account"] == account]
        statistics = [
            ("Duration (days)", (dates[1] - dates[0]).days),
            ("Number of operations", len(df_account.index)),
            ("Minimum operation amount", min(df_account["operation_amount"])),
            ("Maximum operation amount", max(df_account["operation_amount"])),
            ("Average operation amount", round(float(np.mean(df_account["operation_amount"])), 2)),
            ("Total operation amount", round(sum(df_account["operation_amount"]), 2)),
        ]
        for name, result in statistics:
            text = f"{name}: XXX" if anonymous_mode else f"{name}: {result}"
            st.write(text)

    for account in accounts:
        if account != "total":
            st.markdown(f"### {account} account:")
            statistics_account(account=account)
            st.write("")
