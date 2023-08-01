import os
from pathlib import Path

import pandas as pd
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from pyccounting import initialize, orm
from pyccounting._path import _ROOT

initialize.initialize()

st.title("Welcome in Pyccounting 😎")
st.write(f"There are **{len(orm.get_operations())} operations** in total.")

st.write("### Import Operations")

uploaded_file: UploadedFile | None = st.file_uploader(
    label="Upload a file:",
    type=["csv", "xls"],
)
if uploaded_file is not None:
    if "bnp" in uploaded_file.name:
        account: str = "bnp"
    elif "fortuneo" in uploaded_file.name:
        account = "fortuneo"
    else:
        raise ValueError("Couldn't infer account from file name.")
    df: pd.DataFrame = pd.read_csv(uploaded_file, sep=";")

    orm.add_operations(df=df, account=account)
    st.info(f"{len(df)} operations imported.")

    n0: int = len(orm.get_category_operations())
    orm.find_category()
    n1: int = len(orm.get_category_operations())
    st.info(f"{n0 - n1} operation categories found.")

    file_names: list[str] = os.listdir(_ROOT / "data" / "reports")
    idx: int = 1
    while [file_name for file_name in file_names if file_name.startswith(f"{idx}_")]:
        idx += 1
    new_file_name: str = f"{idx}_{uploaded_file.name}"
    with open(_ROOT / "data" / "reports" / new_file_name, "wb") as file:
        file.write(uploaded_file.getbuffer())
    st.info(f"Reports saved as `{new_file_name}`.")

st.write("---")
st.write("### Imported Operations")
file_names = os.listdir(_ROOT / "data" / "reports")
if not file_names:
    st.error("No operation file imported.")
else:
    for file_name in sorted(file_names, key=lambda file_name: int(file_name.split("_")[0])):
        with open(_ROOT / "data" / "reports" / file_name, "rb") as file:
            df = pd.read_csv(file, sep=";")
        with st.expander(label=file_name, expanded=False):
            st.dataframe(df)

st.write("---")
st.write("### Reset Database")
if st.button("Reset"):
    Path.unlink(_ROOT / "data" / "databases" / "sqlite.db")
    st.info("Database reset.")
    initialize.initialize()
