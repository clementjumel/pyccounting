import streamlit as st


def types_widget(extended: bool = False) -> list[str]:
    with st.sidebar:
        options = ["expenses", "incomes"]
        if extended:
            options.append("expenses & incomes")

        st.write("Select the operations type(s):")
        types = [type_ for type_ in options if st.checkbox(type_, value=True)]
        st.write("---")
        return types
