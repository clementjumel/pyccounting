import json
import os
from pathlib import Path

from . import orm
from ._path import _ROOT


def initialize() -> None:
    os.makedirs(_ROOT / "data" / "db", exist_ok=True)
    if Path.exists(_ROOT / "data" / "db" / "sqlite.db"):
        return

    orm.create_tables()

    with open(_ROOT / "data" / "categories.json", "r") as file:
        category_names: list[str] = json.load(file)
    orm.add_categories(category_names=category_names)

    with open(_ROOT / "data" / "rules.json", "r") as file:
        category_rule_contents: dict[str, list[str]] = json.load(file)
    for category_name, rule_contents in category_rule_contents.items():
        orm.add_rules(category_name=category_name, rule_contents=rule_contents)
