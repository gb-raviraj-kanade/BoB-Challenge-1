import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

if "trnasactions_db" not in st.session_state:
    st.session_state["transactions_db"] = pd.read_csv("data/transactions.csv")

st.set_page_config(page_title="Transactions Database", layout="wide")
st.html("<h1 style='text-align: center;'>Transactions Database</h1>")

gob = GridOptionsBuilder.from_dataframe(st.session_state["transactions_db"])
for column in st.session_state["transactions_db"].columns:
    gob.configure_column(column, filter=True, editable=True)
gridOptions = gob.build()
grid_return = AgGrid(st.session_state["transactions_db"],
                    gridOptions=gridOptions,
                    update_mode=GridUpdateMode.GRID_CHANGED)
c1, c2 = st.columns(2)

with c1:
    if st.button("Save"):
        st.session_state["transactions_db"] = grid_return.data
        st.session_state["transactions_db"].to_csv("data/transactions.csv", index=False)

with c2:
    if st.button("Reset"):
        st.session_state["transactions_db"] = pd.read_csv("data/transactions_og.csv")
        st.session_state["transactions_db"].to_csv("data/transactions.csv", index=False)