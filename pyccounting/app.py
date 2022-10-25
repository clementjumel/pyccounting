import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from pyccounting import initialize, orm, widgets
from pyccounting._path import _ROOT

initialize.initialize()

start_date: datetime.date = widgets.start_date()
accounts: list[str] = widgets.accounts()
types: list[str] = widgets.types()
category_names: list[str] = widgets.categories()

st.title("Welcome in Pyccounting 😎")
st.write(f"There are currently **{len(orm.get_operations())} operations** imported in total.")

st.write("### Import Operations")

uploaded_file: UploadedFile | None = st.file_uploader(
    label="Upload a file:",
    type=["csv", "xls"],
)
if uploaded_file is not None:

    if "bnp" in uploaded_file.name:
        account: str = "bnp"
        df: pd.DataFrame = pd.read_csv(uploaded_file, sep=",")
    elif "fortuneo" in uploaded_file.name:
        account = "fortuneo"
        df = pd.read_csv(uploaded_file, sep=";")
        df = df.iloc[::-1]  # reverse the order of the DataFrame
    else:
        raise ValueError("Couldn't infer account from file name.")

    orm.add_operations(df=df, account=account)
    st.info(f"{len(df)} operations imported.")

    n0: int = len(orm.get_category_operations(category_name="unknown"))
    orm.find_category()
    n1: int = len(orm.get_category_operations(category_name="unknown"))
    st.info(f"{n0 - n1} operation's categories found.")

    with open(_ROOT / "data" / "reports" / uploaded_file.name, "wb") as file:
        file.write(uploaded_file.getbuffer())
    st.info("Filed saved.")

if orm.get_operations():

    st.write("### Imported Operations")
    df = orm.get_operation_df(
        start_date=start_date,
        accounts=accounts,
        types=types,
        category_names=category_names,
        date_index=True,
        sort_by_date=True,
    )
    if not df.empty:
        st.write(f"**{len(df)} operations** selected.")
        st.dataframe(df)
    else:
        st.error("There's not operation selected.")

    st.write("### Reboot Operations")
    if st.button("Reboot"):
        Path.unlink(_ROOT / "data" / "databases" / "sqlite.db")
        st.info("Database re-booted.")
        initialize.initialize()
