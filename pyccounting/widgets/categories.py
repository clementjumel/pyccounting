import streamlit as st

from pyccounting import orm


def categories_widget() -> list[str]:
    with st.sidebar:
        options: list[str] = orm.get_category_names()
        category_names: list[str] = st.multiselect(
            label="Select your categories:",
            options=options,
            default=options,
        )
        st.write("---")
        return category_names
