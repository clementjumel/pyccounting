import streamlit as st

from pyccounting import orm


def categories_widget() -> list[str]:
    with st.sidebar:
        df = orm.get_df()
        options = sorted(set(df["category_name"].values))

        category_names: list[str] = st.multiselect(
            label="Select your categories:",
            options=options,
            default=options,
        )
        st.write("---")
        return category_names
