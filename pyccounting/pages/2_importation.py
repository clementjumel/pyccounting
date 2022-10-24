import datetime

import pandas as pd
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from pyccounting import initialize, orm, widgets

initialize.initialize()

dates: tuple[datetime.date, datetime.date] = widgets.dates()
accounts: list[str] = widgets.accounts(extended=False)
types: list[str] = widgets.types(extended=False)
category_names: list[str] = widgets.categories()

st.write("### Import Operations")

account: str = st.radio("Select an account:", ("bnp", "fortuneo"))
uploaded_file: UploadedFile | None = st.file_uploader(
    label="Upload a file:",
    type=["csv", "xls"],
)
if uploaded_file is not None:

    if account == "bnp":
        df: pd.DataFrame = pd.read_csv(uploaded_file, sep=",")
    elif account == "fortuneo":
        df = pd.read_csv(uploaded_file, sep=";")
        df = df.iloc[::-1]  # reverse the order of the DataFrame
    else:
        raise ValueError
    st.dataframe(df)
    orm.add_operations(df=df, account=account)
    orm.find_category()
    st.info(f"{len(df)} operations imported.")

st.write("### Imported Operations")
df = orm.get_operation_df(
    accounts=accounts,
    types=types,
    date_index=True,
    sort_by_date=True,
    dates=dates,
    category_names=category_names,
)
if df.empty:
    st.write("No operation imported, yet.")
else:
    st.write(f"{len(df.index)} operations imported:")
    st.dataframe(df)
