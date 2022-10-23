from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Integer, String

from .base import Base


class Rule(Base):
    __tablename__: str = "rule"

    id_: str = Column(String, primary_key=True, default=lambda x: uuid4().hex)

    idx: int = Column(Integer)
    content: str = Column(String)

    category_id: str = Column(String, ForeignKey("category.id_"))

    def __str___(self) -> str:
        return f"{self.content} ({self.category})"

    def to_dict(self) -> dict:
        return dict(
            idx=self.idx,
            name=self.name,
            categor_namey=self.category.name,
        )

    def match(self, target_tokens: list[str]) -> bool:
        content_tokens = [token.upper() for token in self.content.strip().split()]
        if len(content_tokens) == 1 and content_tokens[0] in target_tokens:
            return True

        target: str = " ".join(target_tokens)
        content: str = " ".join(content_tokens)
        if len(content_tokens) > 1 and content in target:
            return True

        return False
