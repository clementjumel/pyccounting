import os

import streamlit as st
from sqlalchemy.orm import Session

from pyccounting import db


def reset_widget() -> None:
    if os.getenv("RESET_BUTTON") == "1":
        with st.sidebar:
            reset = st.button("Reset")
            st.write("---")
            if reset:
                with Session(db.engine) as session:
                    db.Base.metadata.drop_all(bind=session.bind)
                    db.Base.metadata.create_all(bind=session.bind)
