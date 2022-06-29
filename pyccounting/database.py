from __future__ import annotations

import os

from dotenv import load_dotenv
from sqlalchemy import Column, Date, Float, Integer, String, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, declarative_base

load_dotenv()
engine: Engine = create_engine(url=f"sqlite:///data/db/{os.getenv('DB_NAME')}")

Base = declarative_base()


class Operation(Base):  # type: ignore
    __tablename__ = "operation"

    id_ = Column(Integer, primary_key=True, index=True)
    account = Column(String)
    type_ = Column(String)
    label = Column(String)
    date = Column(Date)
    amount = Column(Float)


os.makedirs("data/db/", exist_ok=True)
with Session(engine) as session:
    Base.metadata.create_all(bind=session.bind)
