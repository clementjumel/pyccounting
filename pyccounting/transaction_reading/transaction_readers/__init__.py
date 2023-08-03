from .abc import TransactionReader
from .bnp import BnpTransactionReader
from .fortuneo import FortuneoTransactionReader

TRANSACTION_READERS: list[TransactionReader] = [
    FortuneoTransactionReader(),
    BnpTransactionReader(),
]
