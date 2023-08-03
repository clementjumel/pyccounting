from pathlib import Path

from ..transaction import Transaction
from .abc import TransactionReader


class BnpTransactionReader(TransactionReader):
    def match_format(self, file_path: Path) -> bool:
        # todo
        return False

    def read(self, file_path: Path) -> list[Transaction]:
        # todo
        return []
