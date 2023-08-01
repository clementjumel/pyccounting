from abc import ABC, abstractmethod

import pandas as pd

from pyccounting.orm.data_model import Transaction


class TransactionReader(ABC):
    """A transaction reader reads tables of transactions and output them as Transaction objects."""

    @abstractmethod
    def match_format(self, df: pd.DataFrame) -> bool:
        """Return True iff the transaction table `df` matches the format of the reader."""
        ...

    @abstractmethod
    def read(self, df: pd.DataFrame) -> list[Transaction]:
        """Return Transaction objects from the transaction table `df`."""
        ...
