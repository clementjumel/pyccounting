import json

import pandas as pd
import streamlit as st

from pyccounting import initialize, orm

initialize.initialize()

category_names: list[str] = orm.get_category_names()

st.title("Welcome in Pyccounting 😎")

st.write("### Categories")
st.write(f"There are {len(category_names)} categories: {', '.join(category_names)}.")

st.write("---")
st.write("### Rules")
category_name: str = st.selectbox(
    "Select a category:",
    options=category_names,
    key="selectbox_0",
)
category_rules: list[orm.Rule] = orm.get_category_rules(category_name=category_name)
rule: orm.Rule = st.selectbox(
    "Select a rule:",
    options=category_rules,
    format_func=lambda rule: rule.content,
    key="selectbox_1",
)
rule_operations: list[orm.Operation] = orm.get_rule_operations(rule_id=rule.id_)
with st.expander(f"{len(rule_operations)} corresponding operations"):
    st.json([operation.to_dict(include_category=False) for operation in rule_operations])

st.write("---")
st.write("### Categories not Found")
df_operation: pd.DataFrame = orm.get_operation_df(category_names=["unknown"]).reset_index(drop=True)
st.write(f"There are **{len(df_operation)} operations** without a category.")
st.dataframe(df_operation)

st.write("---")
st.write("### Add a Rule")
with st.form(key="form_0"):
    category_name = st.selectbox(
        "Select a category:",
        options=category_names,
        key="selectbox_2",
    )
    content: str = st.text_input("Add a content")
    mode: str = st.radio("Select a rule mode:", options=["string", "tokens"])
    if st.form_submit_button("Submit"):
        rule_dict: dict[str, str] = dict(content=content, mode=mode)
        orm.add_rules(category_name=category_name, rule_dicts=[rule_dict])
        st.info("Rule added.")

        n0: int = len(orm.get_category_operations(category_name="unknown"))
        orm.find_category()
        n1: int = len(orm.get_category_operations(category_name="unknown"))
        st.info(f"{n0 - n1} categories found.")

st.write("---")
st.write("### Export Rules")
rule_data: dict[str, list[dict]] = dict()
for category in orm.get_categories():
    rule_data[category.name] = [
        dict(content=rule.content, mode="tokens")
        for rule in orm.get_category_rules(category_name=category.name)
    ]
st.download_button(
    label="Download",
    data=json.dumps(rule_data),
    file_name="rules.json",
)
