from __future__ import annotations

import datetime
from uuid import uuid4

import numpy as np
import pandas as pd
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String

from .base import Base
from .rule import Rule


class Operation(Base):
    __tablename__: str = "operation"

    id_: str = Column(String, primary_key=True, default=lambda x: uuid4().hex)

    idx: int = Column(Integer)
    account: str = Column(String)
    label: str = Column(String)
    date: datetime.date = Column(Date)
    amount: float = Column(Float)

    category_id: str = Column(String, ForeignKey("category.id_"))

    def __str__(self) -> str:
        return f"{self.label} ({self.amount})"

    def to_dict(self) -> dict:
        return dict(
            idx=self.idx,
            account=self.account,
            label=self.label,
            date=self.date,
            amount=self.amount,
            category_name=self.category.name,
        )

    @classmethod
    def from_row(
        cls,
        row: pd.Series,
        account: str,
        idx: int,
        category_id: str,
    ) -> Operation:
        if account == "bnp":
            label: str = row["Libelle operation"].strip()
            if label[-24:-19] == "CARTE":
                label = label[:-24]
            if label.startswith("FACTURE CARTE DU"):
                label = "CARTE" + label.removeprefix("FACTURE CARTE DU")
            label = label.strip()
            date = datetime.datetime.strptime(row["Date operation"], "%d/%m/%Y").date()
            amount = float(row["Montant operation en euro"].replace(",", "."))
        elif account == "fortuneo":
            label = row["libellé"]
            date = datetime.datetime.strptime(row["Date opération"], "%d/%m/%Y").date()
            if row["Débit"] and row["Crédit"] is np.nan:
                amount = float(row["Débit"].replace(",", "."))
            elif row["Crédit"] and row["Débit"] is np.nan:
                amount = float(row["Crédit"].replace(",", "."))
            else:
                raise ValueError
        else:
            raise ValueError

        return cls(
            idx=idx,
            account=account,
            label=label,
            date=date,
            amount=amount,
            category_id=category_id,
        )

    def find_category(self, rules: list[Rule]) -> None:
        target_tokens = [token.upper() for token in self.label.strip().split()]
        for rule in rules:
            if rule.match(target_tokens=target_tokens):
                self.category_id = rule.category_id
                return
