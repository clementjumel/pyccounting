from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

engine: Engine = create_engine(url="sqlite:///data/db/sqlite.db")
