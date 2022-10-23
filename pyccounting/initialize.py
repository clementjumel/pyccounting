import json
import os
from pathlib import Path

from sqlalchemy.orm import Session

from pyccounting import _ROOT, orm


def initialize() -> None:
    os.makedirs(_ROOT / "data" / "db", exist_ok=True)
    if Path.exists(_ROOT / "data" / "db" / "sqlite.db"):
        return

    with Session(orm.engine) as session:
        orm.Base.metadata.create_all(bind=session.bind)

    with open(_ROOT / "data" / "categories.json", "r") as file:
        category_names: list[str] = json.load(file)
    with open(_ROOT / "data" / "rules.json", "r") as file:
        category_rule_contents: dict[str, list[str]] = json.load(file)

    with Session(orm.engine) as session:
        for idx1, category_name in enumerate(category_names):
            category: orm.Category = orm.Category(name=category_name, idx=idx1)
            if category_name in category_rule_contents:
                rule_contents: list[str] = category_rule_contents[category_name]
                for idx2, content in enumerate(rule_contents):
                    category.rules.append(orm.Rule(content=content, idx=idx2))
                session.add(category)
        session.commit()
