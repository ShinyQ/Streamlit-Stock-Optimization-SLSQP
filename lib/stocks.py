import yfinance as yf
import pandas as pd
# https://colab.research.google.com/drive/1w3JxGK8bsRZNM37iH0XUpw8kkfI-uQP-?usp=sharing

stocks_column = ['Date', 'Ticker', 'Close', 'Close Change %']

def calculate_close_price_changes(df):
    # Calculate percentage change in 'Close' column
    df["Close Change %"] = df["Close"].pct_change() * 100

    # Replace NaN with 0 in the 'Close Change %' column
    df["Close Change %"].fillna(0, inplace=True)

    # Round 'Close Change %' to 2 decimal places
    df["Close Change %"] = df["Close Change %"].round(2)

    return df["Close Change %"]


def get_stocks_change_data(stocks, start_period, end_period):
    formatted_df = []
    formatted_stocks = {}
    stock_symbol = []
    
    for stock in stocks:
        stock_symbol.append(stock.split(" - ")[0])
        
    data = yf.download(
        " ".join(stock_symbol), 
        start=start_period, 
        end=end_period, 
        group_by="ticker", 
        interval="1mo"
    )

    for stock in stock_symbol:    
        resetted_index_df = data[stock].reset_index()
        close_change = calculate_close_price_changes(resetted_index_df)
        
        # Adding for optimization
        # Example Result: { "AAPL": [1.12, 4.55, 6.55], "CHV": [2.12, 3.55, 7.55] }
        formatted_stocks[stock] = close_change
        
        # Formatting dataframe for later visualization
        resetted_index_df["Close Change %"] = close_change
        resetted_index_df["Ticker"] = stock
        
        selected_df = resetted_index_df[stocks_column].copy()
        df_list = selected_df.values.tolist()
        formatted_df.extend(df_list) 
        
    new_df = pd.DataFrame(formatted_df, columns=stocks_column)
        
    return formatted_stocks, new_df