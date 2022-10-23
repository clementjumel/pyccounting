from sqlalchemy.orm import Session

from .data_model import Category
from .db import engine


def get_default_category_id() -> str:
    with Session(engine) as session:
        category: Category = session.query(Category).filter(Category.name == "unknown").one()
        return category.id_


def get_category_names() -> list[str]:
    with Session(engine) as session:
        categories: list[Category] = session.query(Category).order_by(Category.idx).all()
        return [category.name for category in categories]
