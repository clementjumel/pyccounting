from streamlit.runtime.uploaded_file_manager import UploadedFile

from ..transaction import Transaction
from .abc import TransactionReader


class FortuneoTransactionReader(TransactionReader):
    def match_format(self, file: UploadedFile) -> bool:
        # todo
        return False

    def read(self, file: UploadedFile) -> list[Transaction]:
        # todo
        return []
