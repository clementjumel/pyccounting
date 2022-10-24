from sqlalchemy.orm import Session

from pyccounting.orm.categories import get_category
from pyccounting.orm.data_model import Category, Operation, Rule
from pyccounting.orm.database import engine
from pyccounting.orm.rules import get_rules


def find_category() -> None:
    rules: list[Rule] = get_rules()
    category: Category = get_category(category_name="unknown")

    with Session(engine) as session:
        operations: list[Operation] = (
            session.query(Operation)
            .filter(Operation.category_id == category.id_)
            .order_by(Operation.idx)
            .all()
        )
        for operation in operations:
            operation.find_category(rules=rules)
        session.commit()
