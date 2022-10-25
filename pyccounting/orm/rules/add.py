from sqlalchemy.orm import Session

from pyccounting.orm.categories import get_category
from pyccounting.orm.data_model import Category, Rule
from pyccounting.orm.database import engine

from .get import get_rule_idx


def add_rules(category_name: str, rule_dicts: list[dict[str, str]]) -> None:
    category: Category = get_category(category_name=category_name)
    idx: int = get_rule_idx(category_name=category_name)
    with Session(engine) as session:
        for offset, rule_dict in enumerate(rule_dicts):
            rule: Rule = Rule(
                content=rule_dict["content"],
                mode=rule_dict["mode"],
                idx=idx + offset,
                category_id=category.id_,
            )
            session.add(rule)
        session.commit()
