import streamlit as st

stocks_compare = st.Page("pages/stocks_compare.py", title="Optimasi Saham Pilihan", icon="📈")

pg = st.navigation([
    stocks_compare, 
])

st.set_page_config(
    page_title="Kelompok 2 Analytics Project - Studi Kasus Optimasi Pada Pilihan Saham Investor", 
    page_icon="💸"
)

pg.run()