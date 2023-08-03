from streamlit.runtime.uploaded_file_manager import UploadedFile

from .transaction import Transaction
from .transaction_readers import TRANSACTION_READERS


def read_transactions(file: UploadedFile) -> list[Transaction]:
    """Read transactions from a file using the first matching transaction reader."""
    for transaction_reader in TRANSACTION_READERS:
        if transaction_reader.match_format(file=file):
            return transaction_reader.read(file=file)

    raise Exception(f"No reader found for `file` '{file}'.")
