import datetime
from typing import Any

import pandas as pd
import streamlit as st


def statistics(
    df: pd.DataFrame,
    dates: tuple[datetime.date, datetime.date],
    accounts: list[str],
    anonymous_mode: bool,
) -> None:
    def display_statistics(stats: dict[str, dict[str, Any]], anonymous_mode: bool) -> None:
        for key_1 in stats:
            for key_2 in stats[key_1]:
                if not anonymous_mode:
                    if isinstance(stats[key_1][key_2], float):
                        stats[key_1][key_2] = round(stats[key_1][key_2], 2)
                    stats[key_1][key_2] = str(stats[key_1][key_2])
                else:
                    stats[key_1][key_2] = "XXX"

        st.dataframe(pd.DataFrame(stats))

    def get_account_stats(df_: pd.DataFrame, statistic_type: str) -> dict[str, Any]:
        if statistic_type == "all":
            pass
        elif statistic_type == "expenses":
            df_ = df_.loc[df_["operation_amount"] < 0]
        elif statistic_type == "incomes":
            df_ = df_.loc[df_["operation_amount"] >= 0]
        else:
            raise ValueError

        return {
            "Num.": len(df_),
            "Num./day": len(df_) / days,
            "Num./month": len(df_) / months,
            "Num./year": len(df_) / years,
            "Max abs. value": max(abs(df_["operation_amount"])),
            "Sum": sum(df_["operation_amount"]),
            "Sum/day": sum(df_["operation_amount"]) / days,
            "Sum/month": sum(df_["operation_amount"]) / months,
            "Sum/year": sum(df_["operation_amount"]) / years,
        }

    st.markdown("### Statistics")

    days = (dates[1] - dates[0]).days
    months = days / 31
    years = days / 365

    st.markdown("#### General")

    account_stats: dict[str, Any] = {
        "Duration in days": days,
        "Duration in months": months,
        "Duration in years": years,
    }
    stats: dict[str, dict[str, Any]] = {"": account_stats}

    display_statistics(stats=stats, anonymous_mode=False)

    for statistic_type in ["all", "expenses", "incomes"]:
        st.markdown(f"#### {statistic_type.capitalize()}")

        stats = {}
        for account in accounts:
            df_account = df.loc[df["account"] == account]
            stats[account] = get_account_stats(df_=df_account, statistic_type=statistic_type)
        if len(accounts) > 1:
            stats["total"] = get_account_stats(df_=df, statistic_type=statistic_type)

        display_statistics(stats=stats, anonymous_mode=anonymous_mode)
