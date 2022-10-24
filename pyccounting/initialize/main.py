from .categories import initialize_categories
from .database import initialize_database
from .operations import initialize_operations
from .rules import initialize_rules


def initialize() -> None:
    initialize_database()
    initialize_categories()
    initialize_rules()
    initialize_operations()
