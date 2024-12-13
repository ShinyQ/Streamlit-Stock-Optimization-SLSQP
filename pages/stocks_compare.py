import streamlit as st
import pandas as pd

from constant.stocks import SNP500, CHOOSEN_STOCKS
from lib.stocks import get_stocks_change_data
from lib.optimization import linear_programming, slsqp_optimization
from components.stocks_visualization import choosen_stocks, visualize_stock_cumulative_percentage

st.title("Optimasi Alokasi Saham Investasi")
st.write(
    """
    Optimisasi pemilihan saham menggunakan metode optimasi SLSQP. 
    Aplikasi ini akan mengoptimalkan alokasi portofolio investasi guna 
    memaksimalkan keuntungan bulanan dengan tetap mematuhi 
    batasan-batasan risiko dan strategi investasi.
"""
)

col1a, col2a = st.columns(2)

with col1a:
    start_date = st.date_input("Masukkan Tanggal Awal:", pd.to_datetime("2021-01-01"))

with col2a:
    end_date = st.date_input("Masukkan Tanggal Akhir:")

stocks = st.multiselect("Pilih saham yang akan di optimisasikan: (min 2)", SNP500, CHOOSEN_STOCKS)

st.subheader("Batasan Alokasi")

col1b, col2b, col3b = st.columns(3)

with col1b:
    allocation = st.number_input(
        "Jumlah investasi: ($)", min_value=250000
    )
    
with col2b:
    proportion = st.number_input(
        "Persentase sama rata: (%)", min_value=0
    )

with col3b:
    tech_stock = st.number_input(
        "Persentase saham teknologi: (%)", min_value=0
    )

col1c, col2c, col3c = st.columns(3)

with col1c:
    non_tech_stock = st.number_input(
        "Persentase saham non teknologi: (%)", min_value=0
    )
    
with col2c:
    oil_gas_stock = st.number_input(
        "Persentase saham migas: (%)", min_value=0
    )

if st.button("Optimisasi Alokasi", type="primary"):
    if not stocks:
        st.error("Semua field harus diisi!")
    elif len(stocks) < 2:
        st.error("Minimal memilih dua saham!")
    elif allocation < 1000:
        st.error("Minimal alokasi investasi adalah $1000!")
    elif proportion == 0 and tech_stock == 0 and non_tech_stock == 0 and oil_gas_stock == 0:
        st.error("Minimal 1 constraint harus diisi!")
    else:
        st.divider()
        
        stocks_formatted, df = get_stocks_change_data(stocks, start_date, end_date)
        
        choosen_stocks(stocks)
        visualize_stock_cumulative_percentage(df, start_date, end_date)
        
        st.divider()
        
        # Menjalankan Kedua Metode dan Menyimpan Hasil Return
        tab1, tab2 = st.tabs(["Linear Programming", "SLSQP Optimization"])
        
        with tab1:
            total_return_lp = linear_programming(
                allocation, 
                stocks_formatted, 
                proportion, 
                tech_stock, 
                non_tech_stock, 
                oil_gas_stock
            )
        
        with tab2:
            total_return_slsqp = slsqp_optimization(
                allocation, 
                stocks_formatted, 
                proportion, 
                tech_stock, 
                non_tech_stock, 
                oil_gas_stock
            )
        
        # Menampilkan Perbandingan Total Return
        st.divider()
        st.subheader("Perbandingan Total Return")

        col1, col2 = st.columns(2)

        with col1:
            if total_return_lp is not None:
                st.metric("Linear Programming Return", f"${round(total_return_lp / 100, 2)}")
            else:
                st.metric("Linear Programming Return", "Gagal")

        with col2:
            if total_return_slsqp is not None:
                st.metric("SLSQP Optimization Return", f"${round(total_return_slsqp / 100, 2)}")
            else:
                st.metric("SLSQP Optimization Return", "Gagal")
