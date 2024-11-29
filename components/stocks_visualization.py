import plotly.graph_objects as go
import streamlit as st
import pandas as pd


def choosen_stocks(stocks):
    st.subheader("Saham Pilihan")

    s = ""

    for stock in stocks:
        s += "- " + stock + "\n"

    st.markdown(s)


def visualize_stock_cumulative_percentage(df, start_date, end_date):
    st.subheader(f'Insight Saham ({start_date} s/d {end_date})')
    
    df_sum = df.copy()
    df_sum.drop('Date', axis=1, inplace=True)

    # Group by Ticker and calculate the sum
    result = df_sum.groupby('Name').sum()[['Volume', 'Close Change %']].sort_values(by='Close Change %', ascending=False)
    st.table(result)
    
    df["Date"] = pd.to_datetime(df["Date"])

    grouped_df = (
        df.groupby(["Name", df["Date"].dt.year])["Close Change %"].sum().reset_index()
    )

    grouped_df["Cumulative Change"] = grouped_df.groupby("Name")[
        "Close Change %"
    ].cumsum()

    fig = go.Figure()
    for ticker, group in grouped_df.groupby("Name"):
        fig.add_trace(
            go.Scatter(
                x=group["Date"],
                y=group["Cumulative Change"],
                mode="lines+markers",
                name=ticker,
                marker=dict(size=8),
            )
        )

    fig.update_layout(
        margin=dict(t=5, b=10, l=0, r=0),
        xaxis_title="Tahun",
        yaxis_title="Persentase Perubahan Kumulatif (%)",
        legend_title="Stocks",
    )

    st.plotly_chart(fig, use_container_width=True)
