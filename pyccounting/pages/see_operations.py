import pandas as pd
import streamlit as st

from pyccounting.database import engine

df = pd.read_sql(sql="operation", con=engine)
df = df[["date", "account", "amount", "label", "type_"]]
df = df.sort_values(by="date", ascending=False)
df["date"] = df["date"].apply(lambda x: x.date())
df = df.set_index("date")

st.dataframe(df)
