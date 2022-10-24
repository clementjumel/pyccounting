from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from pyccounting.orm.data_model import Base

engine: Engine = create_engine(url="sqlite:///data/db/sqlite.db")


def create_tables() -> None:
    with Session(engine) as session:
        Base.metadata.create_all(bind=session.bind)
