import pandas as pd
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
    with Session(db.engine) as session:
        operation = session.query(db.Operation).filter(db.Operation.validated is False).first()

        attrs = ["account", "label", "category"]
        if not anonymous_mode:
            attrs = ["amount"] + attrs
        data = {getattr(operation, attr) for attr in attrs}
        df = pd.DataFrame.from_dict({operation.date: data}, orient="index")
        st.dataframe(df)
        if st.button("Validate"):
            operation.validated = True
            session.commit()
            st.write("Operation validated!")

    df = db.get_df(validated_status=False)
    st.write("---")
    st.write(f"{len(df.index)} operations need a validation:")
    columns = ["account", "label", "category"]
    if not anonymous_mode:
        columns = ["amount"] + columns

    st.dataframe(df[columns])
