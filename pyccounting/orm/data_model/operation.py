import datetime

from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String

from .base import Base
from .category_rule import CategoryRule


class Operation(Base):
    __tablename__ = "operation"

    account: str = Column(String, primary_key=True)
    idx: int = Column(Integer, primary_key=True)

    label: str = Column(String)
    date: datetime.date = Column(Date)
    amount: float = Column(Float)
    category_name: str = Column(String, ForeignKey("category.name"))

    def __str__(self) -> str:
        attr_names: list[str] = ["amount", "date", "label", "account", "category"]
        attrs: list[str] = [str(getattr(self, attr)) for attr in attr_names]
        return ", ".join(attrs)

    def find_category_name(self, category_rules: list[CategoryRule]) -> str:
        target_tokens = [token.upper() for token in self.label.strip().split()]
        for category_rule in category_rules:
            if category_rule.match(target_tokens=target_tokens):
                return category_rule.category_name

        return "unknown"
