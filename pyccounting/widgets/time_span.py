import streamlit as st


def time_span_widget() -> str:
    with st.sidebar:
        time_span = st.radio(
            "Select a time span",
            ["All", "Last year", "Last quarter", "Last month", "Last week"],
        )
        st.write("---")
        return time_span
