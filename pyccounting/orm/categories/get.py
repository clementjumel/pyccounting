from sqlalchemy.orm import Session

from pyccounting.orm.data_model import Category
from pyccounting.orm.database import engine


def get_category(category_name: str) -> Category:
    with Session(engine) as session:
        return session.query(Category).filter(Category.name == category_name).one()


def get_categories() -> list[Category]:
    with Session(engine) as session:
        return session.query(Category).order_by(Category.idx).all()


def get_default_category_id() -> str:
    category: Category = get_category(category_name="unknown")
    return category.id_


def get_category_idx() -> int:
    categories: list[Category] = get_categories()
    if categories:
        return categories[-1].idx + 1
    return 0


def get_category_names() -> list[str]:
    categories: list[Category] = get_categories()
    return [category.name for category in categories]
