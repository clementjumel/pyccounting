from sqlalchemy import Column, ForeignKey, Integer, String

from .base import Base


class CategoryRule(Base):
    __tablename__ = "category_rule"

    category_name: str = Column(String, ForeignKey("category.name"), primary_key=True)
    rule: str = Column(String, primary_key=True)

    idx: int = Column(Integer)

    def __str__(self) -> str:
        attr_names: list[str] = ["idx", "category_name", "rule"]
        attrs: list[str] = [str(getattr(self, attr)) for attr in attr_names]
        return ", ".join(attrs)

    def match(self, target_tokens: list[str]) -> bool:
        content_tokens = [token.upper() for token in self.rule.strip().split()]
        if len(content_tokens) == 1 and content_tokens[0] in target_tokens:
            return True

        target: str = " ".join(target_tokens)
        content: str = " ".join(content_tokens)
        if len(content_tokens) > 1 and content in target:
            return True

        return False
