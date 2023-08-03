from abc import ABC, abstractmethod

from streamlit.runtime.uploaded_file_manager import UploadedFile

from ..transaction import Transaction


class TransactionReader(ABC):
    """A transaction reader reads transactions files and output them as Transaction objects."""

    @abstractmethod
    def match_format(self, file: UploadedFile) -> bool:
        """Return True iff the transaction file matches the format of the reader."""
        ...

    @abstractmethod
    def read(self, file: UploadedFile) -> list[Transaction]:
        """Return Transaction objects from the transaction file."""
        ...
