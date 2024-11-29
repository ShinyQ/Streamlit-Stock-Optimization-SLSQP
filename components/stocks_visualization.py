import plotly.graph_objects as go
import streamlit as st
import pandas as pd

def choosen_stocks(stocks):
    st.subheader("Saham Pilihan")
        
    s = ''

    for stock in stocks:
        s += "- " + stock + "\n"

    st.markdown(s)
    
def visualize_stock_cumulative_percentage(df, ):
    st.subheader("Persentase Perubahan Kumulatif Tahunan (%)")
        
    df["Date"] = pd.to_datetime(df["Date"])

    grouped_df = (
        df.groupby(["Ticker", df["Date"].dt.year])["Close Change %"]
        .sum()
        .reset_index()
    )

    # Create a new column for cumulative sum within each ticker
    grouped_df["Cumulative Change"] = grouped_df.groupby("Ticker")[
        "Close Change %"
    ].cumsum()

    # Create the line chart
    fig = go.Figure()
    for ticker, group in grouped_df.groupby("Ticker"):
        fig.add_trace(
            go.Scatter(
                x=group["Date"],
                y=group["Cumulative Change"],
                mode="lines+markers",
                name=ticker,
                marker=dict(size=8),
            )
        )

    # Customize the layout
    fig.update_layout(
        margin=dict(t=20, b=20, l=0, r=0),
        xaxis_title="Tahun",
        yaxis_title="Persentase Perubahan Kumulatif (%)",
        legend_title="Ticker",
        xaxis_rangeslider_visible=False,  # Hide the range slider
    )

    st.plotly_chart(fig, use_container_width=True)