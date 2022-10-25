from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Rule(Base):
    __tablename__: str = "rule"

    id_: str = Column(String, primary_key=True, default=lambda x: uuid4().hex)

    idx: int = Column(Integer)
    content: str = Column(String)
    mode: str = Column(String)

    category_id: str = Column(String, ForeignKey("category.id_"))
    operations = relationship("Operation")

    def __str___(self) -> str:
        return f"{self.content} ({self.category})"

    def to_dict(self) -> dict:
        return dict(
            idx=self.idx,
            name=self.name,
            categor_namey=self.category.name,
        )

    def match(self, target: str) -> bool:
        content: str = self.content

        target = target.strip().lower()
        content = content.strip().lower()

        if self.mode == "tokens":
            target_tokens: set[str] = set(target.split())
            content_tokens: set[str] = set(content.split())
            if content_tokens.issubset(target_tokens):
                return True

        elif self.mode == "string":
            if content in target:
                return True

        else:
            raise ValueError

        return False
