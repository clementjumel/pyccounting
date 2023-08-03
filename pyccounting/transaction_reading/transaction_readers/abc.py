from abc import ABC, abstractmethod
from pathlib import Path

from ..transaction import Transaction


class TransactionReader(ABC):
    """A transaction reader reads transactions files and output them as Transaction objects."""

    @abstractmethod
    def match_format(self, file_path: Path) -> bool:
        """Return True iff the transaction file matches the format of the reader."""
        ...

    @abstractmethod
    def read(self, file_path: Path) -> list[Transaction]:
        """Return Transaction objects from the transaction file."""
        ...
