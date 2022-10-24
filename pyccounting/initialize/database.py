import os
from pathlib import Path

import streamlit as st

from pyccounting import orm
from pyccounting._path import _ROOT


def initialize_database() -> None:
    os.makedirs(_ROOT / "data" / "databases", exist_ok=True)
    if Path.exists(_ROOT / "data" / "databases" / "sqlite.db"):
        return

    orm.create_tables()
    st.info("Database initialized.")
