import pandas as pd
import streamlit as st

from pyccounting.database import engine

st.dataframe(pd.read_sql(sql="operation", con=engine))
