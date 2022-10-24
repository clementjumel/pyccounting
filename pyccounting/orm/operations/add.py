import pandas as pd
from sqlalchemy.orm import Session

from pyccounting.orm.categories import get_default_category_id
from pyccounting.orm.data_model import Operation
from pyccounting.orm.database import engine

from .get import get_operation_idx


def add_operations(df: pd.DataFrame, account: str) -> None:
    default_category_id: str = get_default_category_id()
    idx: int = get_operation_idx()
    with Session(engine) as session:
        for offset, (_, row) in enumerate(df.iterrows()):
            operation = Operation.from_row(
                row=row,
                account=account,
                idx=idx + offset,
                category_id=default_category_id,
            )
            session.add(operation)
        session.commit()
