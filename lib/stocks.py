import yfinance as yf
import pandas as pd
# https://colab.research.google.com/drive/1w3JxGK8bsRZNM37iH0XUpw8kkfI-uQP-?usp=sharing

stocks_column = ['Date', 'Name', 'Ticker', 'Volume', 'Close', 'Close Change %']

def calculate_close_price_changes(df):
    df["Close Change %"] = df["Close"].pct_change() * 100
    df["Close Change %"] = df["Close Change %"].fillna(0)
    df["Close Change %"] = df["Close Change %"].round(3)

    return df["Close Change %"].to_list()


def get_stocks_change_data(stocks, start_period, end_period):
    formatted_df = []
    stock_symbol = []
    stock_name = []
    
    for stock in stocks:
        stock_split = stock.split(" - ")
        stock_symbol.append(stock_split[0])
        stock_name.append(stock_split[::1][1])
        
    data = yf.download(
        " ".join(stock_symbol), 
        start=start_period, 
        end=end_period, 
        group_by="ticker", 
        interval="1mo"
    )
    
    formatted_stocks = {}
        
    for stock, ticker, name in zip(stocks, stock_symbol, stock_name):    
        resetted_index_df = data[ticker].reset_index()
        close_change = calculate_close_price_changes(resetted_index_df)
        
        # Adding for optimization
        # Example Result: { "AAPL": [1.12, 4.55, 6.55], "CHV": [2.12, 3.55, 7.55] }
        formatted_stocks[stock] = close_change
        
        resetted_index_df["Close Change %"] = close_change
        resetted_index_df["Ticker"] = ticker
        resetted_index_df["Name"] = name
        
        selected_df = resetted_index_df[stocks_column].copy()
        df_list = selected_df.values.tolist()
        formatted_df.extend(df_list) 
        
    new_df = pd.DataFrame(formatted_df, columns=stocks_column)
        
    return formatted_stocks, new_df