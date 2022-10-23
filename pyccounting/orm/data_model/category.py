from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base
from .category_rule import CategoryRule
from .operation import Operation


class Category(Base):
    __tablename__ = "category"

    name: str = Column(String, primary_key=True)

    idx: int = Column(Integer)

    category_rules: list[CategoryRule] = relationship("CategoryRule", backref="category")
    operations: list[Operation] = relationship("Operation", backref="category")

    def __str__(self) -> str:
        attr_names: list[str] = ["idx", "name"]
        attrs: list[str] = [str(getattr(self, attr)) for attr in attr_names]
        return ", ".join(attrs)

    def get_ordered_category_rules(self) -> list[CategoryRule]:
        idxs_and_category_rules: list[tuple[int, CategoryRule]] = [
            (category_rule.idx, category_rule) for category_rule in self.category_rules
        ]
        idxs_and_category_rules = sorted(idxs_and_category_rules)

        category_rules: list[CategoryRule] = [
            idx_and_category_rule[1] for idx_and_category_rule in idxs_and_category_rules
        ]
        return category_rules
