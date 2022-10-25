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
        categories_rule_dicts: dict[str, list[dict[str, str]]] = json.load(file)

    for category_name, rule_dicts in categories_rule_dicts.items():
        orm.add_rules(category_name=category_name, rule_dicts=rule_dicts)
    n: int = sum(len(rule_dicts) for _, rule_dicts in categories_rule_dicts.items())
    st.info(f"{n} rules initialized.")
