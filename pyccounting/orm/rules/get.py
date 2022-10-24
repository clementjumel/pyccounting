from sqlalchemy.orm import Session

from pyccounting.orm.categories import get_category, get_category_names
from pyccounting.orm.data_model import Category, Rule
from pyccounting.orm.database import engine


def get_category_rules(category_name: str) -> list[Rule]:
    category: Category = get_category(category_name=category_name)
    with Session(engine) as session:
        return session.query(Rule).filter(Rule.category_id == category.id_).order_by(Rule.idx).all()


def get_rules() -> list[Rule]:
    rules: list[Rule] = []
    category_names: list[str] = get_category_names()
    for category_name in category_names:
        category_rules: list[Rule] = get_category_rules(category_name=category_name)
        rules.extend(category_rules)
    return rules


def get_rule_idx(category_name: str) -> int:
    rules: list[Rule] = get_category_rules(category_name=category_name)
    if rules:
        return rules[-1].idx + 1
    return 0
