import json
from pathlib import Path

import streamlit as st

from pyccounting import orm
from pyccounting._path import _ROOT


def initialize_categories() -> None:
    if orm.get_categories():
        return
    if not Path.exists(_ROOT / "data" / "categories.json"):
        st.error("No file 'categories.json' found.")
        return

    with open(_ROOT / "data" / "categories.json", "r") as file:
        category_names: list[str] = json.load(file)
    orm.add_categories(category_names)
    n: int = len(category_names)
    st.info(f"{n} categories initialized.")
