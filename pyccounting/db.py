from __future__ import annotations

import streamlit as st
from sqlalchemy import Boolean, Column, Date, Float, Integer, String, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base

engine: Engine = create_engine(url="sqlite:///data/db/sqlite.db")

Base = declarative_base()


class Operation(Base):  # type: ignore
    __tablename__ = "operation"

    id_ = Column(Integer, primary_key=True, index=True)
    account = Column(String, primary_key=True, index=True)
    label = Column(String)
    date = Column(Date)
    amount = Column(Float)
    category = Column(String)
    validated = Column(Boolean)

    def to_string(self, anonymous_mode: bool) -> str:
        attrs = ["date", "label", "account", "category"]
        if not anonymous_mode:
            attrs = ["amount"] + attrs
        return ", ".join([getattr(self, attr) for attr in attrs])

    def set_validated(self, anonymous_mode: bool) -> None:
        self.validated = True
        text = self.to_string(anonymous_mode=anonymous_mode)
        st.write(f"Validation of operation '{text}'.")

    def set_category(self, category: str, anonymous_mode: bool) -> None:
        self.category = category
        text = self.to_string(anonymous_mode=anonymous_mode)
        st.write(f"Category '{category}' set for operation '{text}'.")

    def apply_category_rules(
        self,
        category_rules: list[CategoryRule],
        anonymous_mode: bool,
    ) -> None:
        if self.category != "":
            return

        target_tokens = [token.upper() for token in self.label.strip().split()]
        target = " ".join(target_tokens)
        for category_rule in category_rules:
            content_tokens = [token.upper() for token in category_rule.content.strip().split()]
            content = " ".join(content_tokens)

            match = False
            if len(content_tokens) == 1 and content_tokens[0] in target_tokens:
                match = True
            elif len(content_tokens) > 1 and content in target:
                match = True

            if match:
                self.set_category(
                    category=category_rule.category,
                    anonymous_mode=anonymous_mode,
                )
                return


class CategoryRule(Base):  # type: ignore
    __tablename__ = "category_rule"

    category = Column(String, primary_key=True, index=True)
    content = Column(String, primary_key=True, index=True)
