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
                operation.apply_category_rules(
                    category_rules=[category_rule],
                    anonymous_mode=anonymous_mode,
                )

            session.commit()

if not df.empty:
    with st.form("category_selection"):
        st.write("You can manually mark the remaining operations:")
        category = st.selectbox("Select a category: ", CATEGORIES)

        with Session(db.engine) as session:
            query = session.query(db.Operation).filter(db.Operation.category == "")
            operations = query.all()[:10]

        operations_dict: dict[int, db.Operation] = {
            operation.id_: operation for operation in operations
        }
        checks: dict[int, bool] = {}
        for id_, operation in operations_dict.items():
            checks[id_] = st.checkbox(
                label=operation.to_string(anonymous_mode=anonymous_mode),
                value=False,
                key=f"category_selection_{id_}",
            )

        if st.form_submit_button("Submit"):
            with Session(db.engine) as session:
                for id_ in checks:
                    if checks[id_]:
                        query = session.query(db.Operation).filter(db.Operation.id_ == id_)
                        operation = query.one()
                        operation.set_category(category=category, anonymous_mode=anonymous_mode)

                session.commit()

            st.experimental_rerun()
