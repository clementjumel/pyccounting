import os

import streamlit as st


def anonymous_mode_widget() -> bool:
    with st.sidebar:
        anonymous_mode = st.checkbox("Anonymous mode", value=os.getenv("ANONYMOUS_MODE") == "1")
        st.write("---")
        return anonymous_mode
