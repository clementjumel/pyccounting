import datetime
from typing import Any

import pandas as pd
import streamlit as st


def _get_account_stats(
    df: pd.DataFrame,
    days: int,
    months: float,
    years: float,
) -> dict[str, Any]:
    return {
        "Num.": len(df),
        "Num./day": len(df) / days,
        "Num./month": len(df) / months,
        "Num./year": len(df) / years,
        "Max value": max(df["operation_amount"]),
        "Sum": sum(df["operation_amount"]),
        "Sum/day": sum(df["operation_amount"]) / days,
        "Sum/month": sum(df["operation_amount"]) / months,
        "Sum/year": sum(df["operation_amount"]) / years,
    }


def _display_stats(stats: dict[str, dict[str, Any]], anonymous_mode: bool) -> None:
    for key_1 in stats:
        for key_2 in stats[key_1]:

            if not anonymous_mode:
                if isinstance(stats[key_1][key_2], float):
                    stats[key_1][key_2] = round(stats[key_1][key_2], 2)
                stats[key_1][key_2] = str(stats[key_1][key_2])
            else:
                stats[key_1][key_2] = "XXX"

    df = pd.DataFrame(stats)
    st.dataframe(df)


def statistics(
    df: pd.DataFrame,
    dates: tuple[datetime.date, datetime.date],
    accounts: list[str],
    types: list[str],
    anonymous_mode: bool,
) -> None:
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

    _display_stats(stats=stats, anonymous_mode=False)

    for type_ in types:
        st.markdown(f"#### {type_.capitalize()}")
        stats = {}
        for account in accounts:

            df_ = df.loc[df["account"] == account] if account != "total" else df
            if type_ == "expenses":
                df_ = -1 * df_.loc[df_["operation_amount"] < 0]
            elif type_ == "incomes":
                df_ = df_.loc[df_["operation_amount"] >= 0]
            elif type_ == "expenses & incomes":
                pass
            else:
                raise ValueError

            stats[account] = _get_account_stats(
                df=df_,
                days=days,
                months=months,
                years=years,
            )

        _display_stats(stats=stats, anonymous_mode=anonymous_mode)
