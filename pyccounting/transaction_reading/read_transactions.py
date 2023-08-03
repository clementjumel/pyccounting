from pathlib import Path

from .transaction import Transaction
from .transaction_readers import TRANSACTION_READERS


def read_transactions(file_path: Path) -> list[Transaction]:
    """Read transactions from a file using the first matching transaction reader."""
    for transaction_reader in TRANSACTION_READERS:
        if transaction_reader.match_format(file_path=file_path):
            return transaction_reader.read(file_path=file_path)

    raise Exception(f"No reader found for `file_path` '{file_path}'.")
