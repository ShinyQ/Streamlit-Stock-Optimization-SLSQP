import streamlit as st

from constant.stocks import SNP500
from lib.stocks import get_stocks_change_data
st.header("Optimasi Pemilihan Saham")

modal = st.text_input("Masukkan Jumlah Uang Yang Ingin Diinvestasikan:")
stocks = st.multiselect("Pilih saham S&P500 yang akan di optimisasikan", SNP500)
st.write("You selected:", stocks)

if stocks:
   test, test1 = get_stocks_change_data(stocks, "2022-01-01", "2024-01-01")
   st.write(test, test1)