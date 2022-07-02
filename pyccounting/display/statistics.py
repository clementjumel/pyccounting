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
    def statistics_df(df_: pd.DataFrame) -> None:
        statistics = [
            ("Duration (days)", (dates[1] - dates[0]).days),
            ("Number of operations", len(df_.index)),
            ("Minimum operation amount", min(df_["operation_amount"])),
            ("Maximum operation amount", max(df_["operation_amount"])),
            ("Average operation amount", round(float(np.mean(df_["operation_amount"])), 2)),
            ("Total operation amount", round(sum(df_["operation_amount"]), 2)),
        ]
        for name, result in statistics:
            text = f"{name}: XXX" if anonymous_mode else f"{name}: {result}"
            st.write(text)

    for account in accounts:
        st.markdown(f"#### {account} account:")
        df_account = df.loc[df["account"] == account]
        statistics_df(df_=df_account)
    if len(accounts) > 1:
        st.markdown("#### Total")
        statistics_df(df_=df)
