import streamlit as st

stocks_compare = st.Page("pages/stocks_compare.py", title="Optimasi Saham Pilihan", icon="📈")
example_page = st.Page("pages/example.py", title="Example Page", icon=":material/delete:")

pg = st.navigation([
    stocks_compare, 
    example_page
])

st.set_page_config(
    page_title="Kelompok 2 Analytics Project - Studi Kasus Optimasi Pada Pilihan Saham Investor", 
    page_icon="💸"
)

pg.run()