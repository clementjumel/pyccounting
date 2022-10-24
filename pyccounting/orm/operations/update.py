from sqlalchemy.orm import Session

from pyccounting.orm.data_model import Operation, Rule
from pyccounting.orm.database import engine
from pyccounting.orm.rules import get_rules

from .get import get_category_operations


def find_category() -> None:
    rules: list[Rule] = get_rules()
    with Session(engine) as session:
        operations: list[Operation] = get_category_operations(category_name="unknown")
        for operation in operations:
            operation.find_category(rules=rules)
        session.commit()
