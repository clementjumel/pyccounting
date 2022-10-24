from sqlalchemy.orm import Session

from pyccounting.orm.data_model import Rule
from pyccounting.orm.database import engine

from .get import get_rule_idx


def add_rules(category_name: str, rule_contents: list[str]) -> None:
    idx: int = get_rule_idx(category_name=category_name)
    with Session(engine) as session:
        for offset, rule_content in enumerate(rule_contents):
            rule: Rule = Rule(content=rule_content, idx=idx + offset)
            session.add(rule)
        session.commit()
