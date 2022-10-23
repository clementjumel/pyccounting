from uuid import uuid4

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base
from .operation import Operation
from .rule import Rule


class Category(Base):
    __tablename__: str = "category"

    id_: str = Column(String, primary_key=True, default=lambda x: uuid4().hex)

    idx: int = Column(Integer)
    name: str = Column(String)

    rules: list[Rule] = relationship("Rule", backref="category")
    operations: list[Operation] = relationship("Operation", backref="category")

    def __str__(self) -> str:
        return self.name

    def to_dict(self) -> dict:
        return dict(
            idx=self.idx,
            name=self.name,
        )

    def get_rules(self) -> list[Rule]:
        return sorted(self.rules, key=lambda rule: rule.idx)

    def get_operations(self) -> list[Operation]:
        return sorted(self.operations, key=lambda operation: operation.idx)
