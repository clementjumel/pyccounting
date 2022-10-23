from sqlalchemy.orm import Session

from .data_model import Category, Rule
from .db import engine


def get_rules() -> list[Rule]:
    with Session(engine) as session:
        rules: list[Rule] = []
        categories: list[Category] = session.query(Category).order_by(Category.idx).all()
        for category in categories:
            rules.extend(category.get_rules())
        return rules
