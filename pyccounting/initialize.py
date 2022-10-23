import os

from sqlalchemy.orm import Session

from pyccounting import _ROOT

from .db import Base, engine


def initialize() -> None:
    os.makedirs(_ROOT / "data" / "db", exist_ok=True)
    with Session(engine) as session:
        Base.metadata.create_all(bind=session.bind)
