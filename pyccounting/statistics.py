import numpy as np
import pandas as pd
import streamlit as st


def _statistics_account(df_account: pd.DataFrame, anonymous_mode: bool) -> None:
    statistics = [
        ("Number of operations", len(df_account.index)),
        ("Minimum operation amount", min(df_account["operation_amount"])),
        ("Maximum operation amount", max(df_account["operation_amount"])),
        ("Average operation amount", round(float(np.mean(df_account["operation_amount"])), 2)),
        ("Total operation amount", round(sum(df_account["operation_amount"]), 2)),
    ]
    for name, result in statistics:
        text = f"{name}: XXX" if anonymous_mode else f"{name}: {result}"
        st.write(text)


def statistics(df: pd.DataFrame, accounts: list[str], anonymous_mode: bool) -> None:
    for account in accounts:
        if account != "total":
            st.markdown(f"### {account} account:")
            df_account = df.loc[df["account"] == account]
            _statistics_account(df_account=df_account, anonymous_mode=anonymous_mode)
            st.write("")

        else:
            st.write("### Total:")
            _statistics_account(df_account=df, anonymous_mode=anonymous_mode)
            st.write("")
