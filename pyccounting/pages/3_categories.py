import streamlit as st
from sqlalchemy.orm import Session

from pyccounting import db, widgets

anonymous_mode: bool = widgets.anonymous_mode()
widgets.reset()

CATEGORIES = [
    "restaurant & bars",
    "groceries",
    "clothes",
    "shopping",
    "sport",
    "culture",
    "daily life",
    "travel",
    "housing",
    "health",
    "salary",
    "reimbursement",
    "transfer",
    "taxes",
    "other",
]

st.write("### Categories")

df = db.get_df(date_index=False, categories=[""])

if df.empty:
    st.write("All the operations have a category.")

else:
    st.write(f"The following {len(df.index)} operations have no category:")
    columns = ["date", "account", "label"]
    if not anonymous_mode:
        columns = ["amount"] + columns
    st.dataframe(df[columns])

with st.form("category_rule"):
    st.write("You can add a new category rule:")
    kwargs = {
        "category": st.selectbox("Select a category:", CATEGORIES),
        "content": st.text_input("Add a content:"),
    }
    if st.form_submit_button("Submit"):
        with Session(db.engine) as session:
            category_rule = db.CategoryRule(**kwargs)
            session.add(category_rule)

            operations = session.query(db.Operation).filter(db.Operation.category == "").all()
            for operation in operations:
                operation.apply_category_rules(category_rules=[category_rule])

            session.commit()

if not df.empty:
    with st.form("category_selection"):
        st.write("You can manually mark the remaining operations:")
        category = st.selectbox("Select a category: ", CATEGORIES)
        with Session(db.engine) as session:
            operations = session.query(db.Operation).filter(db.Operation.category == "").all()
            operation_labels = [operation.label for operation in operations[:10]]

        checks: dict[str, bool] = {}
        for i, operation_label in enumerate(operation_labels):
            checks[operation_label] = st.checkbox(
                label=operation_label,
                value=False,
                key=f"{i}_{operation_label}",
            )

        if st.form_submit_button("Submit"):
            with Session(db.engine) as session:
                cmpt = 0
                operations = session.query(db.Operation).filter(db.Operation.category == "").all()
                for operation in operations:
                    if operation.label in checks and checks[operation.label]:
                        operation.category = category
                        cmpt += 1

                session.commit()
            st.write(f"{cmpt} operation categories set to {category}.")
