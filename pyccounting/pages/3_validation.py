import streamlit as st
from sqlalchemy.orm import Session

from pyccounting import db, widgets

anonymous_mode: bool = widgets.anonymous_mode()
widgets.reset()

st.write("### Validation")

df = db.get_df(validated_status=False)

if df.empty:
    st.write("There's no operation needing validation! 😊")

else:
    df = db.get_df(validated_status=False)
    st.write(f"{len(df.index)} operations need a validation:")
    columns = ["account", "label", "category"]
    if not anonymous_mode:
        columns = ["amount"] + columns
    st.dataframe(df[columns])

    st.write("---")

    with st.form("validation"):
        st.write("You can validate the remaining operations:")

        with Session(db.engine) as session:
            query = session.query(db.Operation).filter(db.Operation.validated is False)
            operations = query.all()[:10]

        operations_dict: dict[int, db.Operation] = {
            operation.id_: operation for operation in operations
        }
        checks: dict[int, bool] = {}
        for id_, operation in operations_dict.items():
            checks[id_] = st.checkbox(
                label=operation.to_string(anonymous_mode=anonymous_mode),
                value=False,
                key=f"validation_{id_}",
            )

        if st.form_submit_button("Submit"):
            with Session(db.engine) as session:
                for id_ in checks:
                    if checks[id_]:
                        query = session.query(db.Operation).filter(db.Operation.id_ == id_)
                        operation = query.one()
                        operation.set_validated(anonymous_mode=anonymous_mode)

                session.commit()

            st.experimental_rerun()
