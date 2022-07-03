import pandas as pd
import streamlit as st
from sqlalchemy.orm import Session

from pyccounting import db

df = pd.read_sql(sql="category_rule", con=db.engine)

st.write(f"{len(df.index)} rules:")
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
