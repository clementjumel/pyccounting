import os

import streamlit as st


def anonymous_mode_widget() -> bool:
    if os.getenv("ANONYMOUS_MODE") == "1":
        with st.sidebar:
            anonymous_mode = st.checkbox("Anonymous mode", value=True)
            st.write("---")
            return anonymous_mode

    return False
