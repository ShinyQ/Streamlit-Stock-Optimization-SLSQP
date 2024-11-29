import streamlit as st
import pandas as pd

from constant.stocks import SNP500
from lib.stocks import get_stocks_change_data
from components.stocks_visualization import choosen_stocks, visualize_stock_cumulative_percentage

st.title("Optimasi Pemilihan Saham")
st.write(
    """
    Optimisasi pemilihan saham menggunakan metode optimasi SQLSP. 
    Aplikasi ini akan mengoptimalkan alokasi portofolio investasi guna 
    memaksimalkan keuntungan bulanan dengan tetap mematuhi 
    batasan-batasan risiko dan strategi investasi.
"""
)

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input("Masukkan Tanggal Awal:", pd.to_datetime("2019-01-01"))

with col2:
    end_date = st.date_input("Masukkan Tanggal Akhir:")

stocks = st.multiselect("Pilih saham yang akan di optimisasikan: (min 2)", SNP500)

modal = st.number_input(
    "Masukkan Jumlah Uang Yang Ingin Diinvestasikan:", min_value=1000
)

if st.button("Optimisasi Alokasi", type="primary"):
    if not stocks or modal < 1000:
        st.error("Semua field harus diisi!")
    elif len(stocks) < 2:
        st.error("Minimal memilih dua saham!")
    else:
        stocks_formatted, df = get_stocks_change_data(stocks, start_date, end_date)
        choosen_stocks(stocks)
        visualize_stock_cumulative_percentage(df)
