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
        "Max value": max(df["amount"]) if not df["amount"].empty else 0,
        "Sum": sum(df["amount"]),
        "Sum/day": sum(df["amount"]) / days,
        "Sum/month": sum(df["amount"]) / months,
        "Sum/year": sum(df["amount"]) / years,
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
    start_date: datetime.date,
    accounts: list[str],
    types: list[str],
) -> None:
    st.write("### Statistics")

    days = (datetime.date.today() - start_date).days
    months = days / 31
    years = days / 365

    st.write("#### General")

    account_stats: dict[str, Any] = {
        "Duration in days": days,
        "Duration in months": months,
        "Duration in years": years,
    }
    stats: dict[str, dict[str, Any]] = {"": account_stats}

    _display_stats(stats=stats, anonymous_mode=False)

    for type_ in types:
        st.write(f"#### {type_.capitalize()}")
        stats = {}
        for account in accounts:
            df_ = df.loc[df["account"] == account] if account != "total" else df
            if type_ == "expenses":
                df_ = -1 * df_.loc[df_["amount"] < 0]
            elif type_ == "incomes":
                df_ = df_.loc[df_["amount"] >= 0]
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

        _display_stats(stats=stats, anonymous_mode=False)
