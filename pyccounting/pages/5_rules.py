import json

import pandas as pd
import streamlit as st
from sqlalchemy.orm import Session

from pyccounting import db, widgets

widgets.reset()

df = pd.read_sql(sql="category_rule", con=db.engine)

st.write(f"There are {len(df.index)} category rules:")
st.dataframe(df)

st.write("---")
st.write("You can delete an existing category rule:")

category = st.selectbox("Select a category:", sorted(set(df["category"])))
content = st.selectbox(
    "Add a content:",
    sorted(set(df.loc[df["category"] == category]["content"])),
)

if st.button("Submit"):
    with Session(db.engine) as session:
        category_rule = (
            session.query(db.CategoryRule)
            .filter(db.CategoryRule.category == category, db.CategoryRule.content == content)
            .one()
        )

        session.delete(category_rule)
        session.commit()
        st.write("Rule deleted.")
        st.experimental_rerun()

st.write("---")
uploaded_file = st.file_uploader(label="You can also upload rules from a file:", type=[".json"])
if uploaded_file is not None:
    li = json.load(uploaded_file)
    if not isinstance(li, list):
        raise TypeError

    category_rules = []
    for d in li:
        if not isinstance(d, dict):
            raise TypeError
        category_rule = db.CategoryRule(category=d["category"], content=d["content"])
        category_rules.append(category_rule)

    with Session(db.engine) as session:
        session.add_all(category_rules)
        session.commit()

st.write("Or download the existing rules:")
with Session(db.engine) as session:
    query = session.query(db.CategoryRule)
    category_rules = query.all()
    data = [
        {"category": category_rule.category, "content": category_rule.content}
        for category_rule in category_rules
    ]

st.download_button(label="Download", data=json.dumps(data), file_name="category_rules.json")
