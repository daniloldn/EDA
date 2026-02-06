import streamlit as st
import sqlite3
import pandas as pd

@st.cache_resource
def get_conn(db_path: str):
    return sqlite3.connect(db_path, check_same_thread=False)

conn = get_conn("data/nba.sqlite")

query = st.text_area("SQL query", "SELECT * FROM game LIMIT 50;")
df = pd.read_sql_query(query, conn)
st.dataframe(df)