from .bnp import BnpTransactionReader
from .fortuneo import FortuneoTransactionReader

TRANSACTION_READERS = [
    FortuneoTransactionReader(),
    BnpTransactionReader(),
]
