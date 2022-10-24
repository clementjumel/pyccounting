import json
from pathlib import Path

import streamlit as st

from pyccounting import orm
from pyccounting._path import _ROOT


def initialize_rules() -> None:
    if orm.get_rules():
        return
    if not Path.exists(_ROOT / "data" / "rules.json"):
        st.error("No file 'rules.json' found.")
        return

    with open(_ROOT / "data" / "rules.json", "r") as file:
        category_rule_contents: dict[str, list[str]] = json.load(file)
    for category_name, rule_contents in category_rule_contents.items():
        orm.add_rules(category_name=category_name, rule_contents=rule_contents)
    n: int = sum(len(rule_contents) for _, rule_contents in category_rule_contents.items())
    st.info(f"{n} rules initialized.")
