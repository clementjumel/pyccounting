import os

import pandas as pd
import streamlit as st

from pyccounting import orm
from pyccounting._path import _ROOT


def initialize_operations() -> None:
    os.makedirs(_ROOT / "data" / "reports", exist_ok=True)
    if orm.get_operations():
        return

    for report_path in (_ROOT / "data" / "reports").glob("*.csv"):
        if "bnp" in str(report_path):
            account: str = "bnp"
            df: pd.DataFrame = pd.read_csv(report_path, sep=",")
        elif "fortuneo" in str(report_path):
            account = "fortuneo"
            df = pd.read_csv(report_path, sep=";")
            df = df.iloc[::-1]  # reverse the order of the DataFrame
        else:
            raise ValueError("Couldn't infer account from file name.")

        orm.add_operations(df=df, account=account)
        st.info(f"{len(df)} operations imported.")

        n0: int = len(orm.get_category_operations(category_name="unknown"))
        orm.find_category()
        n1: int = len(orm.get_category_operations(category_name="unknown"))
        st.info(f"{n0 - n1} operation categories found.")
