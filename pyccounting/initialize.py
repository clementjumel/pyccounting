import json
import os
from pathlib import Path

from sqlalchemy.orm import Session

from pyccounting import _ROOT, orm


def initialize() -> None:
    os.makedirs(_ROOT / "data" / "db", exist_ok=True)
    if not Path.exists(_ROOT / "data" / "db" / "sqlite.db"):
        with Session(orm.engine) as session:
            orm.Base.metadata.create_all(bind=session.bind)

        with open(_ROOT / "data" / "categories.json", "r") as file:
            category_names: list[str] = json.load(file)
        categories: list[orm.Category] = [
            orm.Category(name=category_name, idx=idx)
            for idx, category_name in enumerate(category_names)
        ]

        with open(_ROOT / "data" / "rules.json", "r") as file:
            rules: dict[str, list[str]] = json.load(file)
        category_rules: list[orm.CategoryRule] = [
            orm.CategoryRule(category_name=category_name, rule=rule, idx=idx)
            for category_name, rules_ in rules.items()
            for idx, rule in enumerate(rules_)
        ]

        with Session(orm.engine) as session:
            session.add_all(categories)
            session.add_all(category_rules)
            session.commit()
