import pandas as pd

from pyccounting.orm.data_model import Transaction

from .abc import TransactionReader


class BnpTransactionReader(TransactionReader):
    def match_format(self, df: pd.DataFrame) -> bool:
        # todo
        return False

    def read(self, df: pd.DataFrame) -> list[Transaction]:
        # todo
        return []
