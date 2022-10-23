import json
from collections import defaultdict

import pandas as pd
import streamlit as st
from sqlalchemy.orm import Session

from pyccounting import initialize, orm

initialize.initialize()

st.write("### Categories")

with Session(orm.engine) as session:
    categories: list[orm.Category] = session.query(orm.Category).all()
attr_names: list[str] = ["idx", "name"]
df: pd.DataFrame = pd.DataFrame(
    data=[
        {attr_name: getattr(category, attr_name) for attr_name in attr_names}
        for category in categories
    ]
)
df = df.set_index("idx")
st.dataframe(df)

st.write("### Rules")

category_rules: list[orm.CategoryRule] = session.query(orm.CategoryRule).all()
attr_names = ["idx", "category_name", "rule"]
df = pd.DataFrame(
    data=[
        {attr_name: getattr(category_rule, attr_name) for attr_name in attr_names}
        for category_rule in category_rules
    ]
)
st.dataframe(df)
category_names = list(set(df["category_name"]))

df = orm.get_df(date_index=False, category_names=["unknown"])

if df.empty:
    st.write("All the operations have a category! 🥳")

else:
    st.write(f"The following {len(df.index)} operations have no category:")
    columns = ["amount", "date", "account", "label"]
    st.dataframe(df[columns])

with st.form("category_rule"):
    st.write("You can add a new category rule:")
    kwargs = {
        "category_name": st.selectbox("Select a category:", category_names),
        "rule": st.text_input("Add a rule:"),
    }
    if st.form_submit_button("Submit"):
        with Session(orm.engine) as session:
            category_rules = (
                session.query(orm.CategoryRule)
                .filter(orm.CategoryRule.category_name == kwargs["category_name"])
                .all()
            )
            idx = max(category_rule.idx for category_rule in category_rules) + 1
            category_rule = orm.CategoryRule(**kwargs, idx=idx)
            session.add(category_rule)

            operations = (
                session.query(orm.Operation).filter(orm.Operation.category_name == "unknown").all()
            )
            for operation in operations:
                operation.find_category_name(category_rules=[category_rule])
            session.commit()

df = pd.read_sql(sql="category_rule", con=orm.engine)

st.write("---")
st.write("You can delete an existing category rule:")

category_name = st.selectbox("Select a category:", sorted(set(df["category_name"])))
rule = st.selectbox(
    "Add a rule:",
    sorted(set(df.loc[df["category_name"] == category_name]["rule"])),
)

if st.button("Submit"):
    with Session(orm.engine) as session:
        category_rule = (
            session.query(orm.CategoryRule)
            .filter(orm.CategoryRule.category_name == category_name, orm.CategoryRule.rule == rule)
            .one()
        )

        session.delete(category_rule)
        session.commit()
        st.write("Rule deleted.")
        st.experimental_rerun()

st.write("---")
st.write("Or download the categories:")
with Session(orm.engine) as session:
    categories = session.query(orm.Category).all()
    idxs_and_categories: list[tuple[int, str]] = [
        (category.idx, category.name) for category in categories
    ]
    idxs_and_categories = sorted(idxs_and_categories)
    data = [idx_and_category[1] for idx_and_category in idxs_and_categories]
st.download_button(label="Download", data=json.dumps(data), file_name="categories.json")

st.write("or download the existing rules:")
with Session(orm.engine) as session:
    category_rules = session.query(orm.CategoryRule).all()
    data_ = defaultdict(list)
    for category_rule in category_rules:
        data_[category_rule.category_name].append(category_rule.rule)
st.download_button(label="Download", data=json.dumps(data_), file_name="category_rules.json")
