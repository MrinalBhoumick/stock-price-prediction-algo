import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Set the page configuration
st.set_page_config(page_title="Stock Prediction App", layout="wide")

# Sidebar for user input
st.sidebar.header("Input Options")
ticker_symbol = st.sidebar.text_input("Enter Stock Ticker Symbol", "AAPL")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("today"))
moving_avg_window = st.sidebar.slider("Moving Average Window (Days)", 5, 50, 20)

# Title
st.title("📈 Simple Stock Prediction App")

# Fetch data from Yahoo Finance
@st.cache_data
def fetch_data(ticker, start, end):
    stock_data = yf.download(ticker, start=start, end=end)
    return stock_data

# Display stock data
try:
    stock_data = fetch_data(ticker_symbol, start_date, end_date)
    st.write(f"### {ticker_symbol} Stock Data from {start_date} to {end_date}")
    st.dataframe(stock_data.tail())

    # Plot stock closing prices
    st.write("### Closing Price Over Time")
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data["Close"], label="Close Price", color="blue")
    plt.title(f"{ticker_symbol} Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    st.pyplot(plt)

    # Add Moving Average
    stock_data[f"MA_{moving_avg_window}"] = stock_data["Close"].rolling(window=moving_avg_window).mean()
    st.write(f"### {moving_avg_window}-Day Moving Average")
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data["Close"], label="Close Price", color="blue", alpha=0.6)
    plt.plot(stock_data[f"MA_{moving_avg_window}"], label=f"{moving_avg_window}-Day MA", color="orange")
    plt.title(f"{ticker_symbol} Price with {moving_avg_window}-Day Moving Average")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    st.pyplot(plt)

    # Simple prediction (trend analysis based on moving average)
    if stock_data[f"MA_{moving_avg_window}"].iloc[-1] > stock_data[f"MA_{moving_avg_window}"].iloc[-2]:
        st.write("🔼 **Prediction**: The stock is in an upward trend based on the moving average.")
    else:
        st.write("🔽 **Prediction**: The stock is in a downward trend based on the moving average.")

except Exception as e:
    st.error(f"An error occurred: {e}")
