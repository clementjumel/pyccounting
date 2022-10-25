from pathlib import Path

import pandas as pd
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from pyccounting import initialize, orm
from pyccounting._path import _ROOT

initialize.initialize()

st.title("Welcome in Pyccounting 😎")
st.write(f"There are currently **{len(orm.get_operations())} operations** imported.")

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
    orm.add_operations(df=df, account=account)
    orm.find_category()
    st.info(f"{len(df)} operations imported.")

    with open(_ROOT / "data" / "reports" / uploaded_file.name, "wb") as file:
        file.write(uploaded_file.getbuffer())
    st.info("Filed saved.")

df = orm.get_operation_df(date_index=True, sort_by_date=True)
if not df.empty:
    st.write("### Imported Operations")
    st.dataframe(df)

    st.write("### Reboot Operations")
    if st.button("Reboot"):
        Path.unlink(_ROOT / "data" / "databases" / "sqlite.db")
        st.info("Database re-booted")
        initialize.initialize()
