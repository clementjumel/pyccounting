from sqlalchemy.orm import Session

from pyccounting.orm.data_model import Category
from pyccounting.orm.database import engine

from .get import get_category_idx


def add_categories(category_names: list[str]) -> None:
    idx: int = get_category_idx()
    with Session(engine) as session:
        for offset, category_name in enumerate(category_names):
            category: Category = Category(name=category_name, idx=idx + offset)
            session.add(category)
        session.commit()
