from sqlalchemy.orm import Session

from pyccounting.orm.categories import get_category
from pyccounting.orm.data_model import Category, Rule
from pyccounting.orm.database import engine


def update_rule(rule_id: str, content: str, mode: str) -> None:
    default_category: Category = get_category()
    with Session(engine) as session:
        rule: Rule = session.query(Rule).filter(Rule.id_ == rule_id).one()

        for operation in rule.operations:
            operation.category_id = default_category.id_
        rule.content = content
        rule.mode = mode

        session.commit()
