import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set the title and subtitle
st.title("Crypto and Stock Price Analysis with Basic Trading Strategy")
st.write("A Streamlit app for historical price display, analysis, and basic trading strategy simulation.")

# Sidebar
st.sidebar.subheader("Select Asset and Time Period")

# Input for selecting asset (stock or crypto)
asset_type = st.sidebar.selectbox("Select Asset Type:", ["Stock", "Crypto"])

# Input for selecting ticker
ticker = st.sidebar.text_input("Enter Ticker Symbol (e.g., AAPL, BTC-USD):", "AAPL" if asset_type == "Stock" else "BTC-USD")

# Input for selecting date range
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2023-12-31"))

# Download historical data
if asset_type == "Stock":
    data = yf.download(ticker, start=start_date, end=end_date)
else:
    # For crypto data, you would use a different data source or API
    # For simplicity, we assume crypto data is similar in structure to stock data
    data = yf.download(ticker, start=start_date, end=end_date)

# Display historical data
st.subheader(f"Historical {ticker} Data")
st.write(data)

# Simple Moving Average (SMA) trading strategy
def sma_strategy(data, short_window, long_window):
    data["Short_MA"] = data["Close"].rolling(window=short_window).mean()
    data["Long_MA"] = data["Close"].rolling(window=long_window).mean()
    data["Signal"] = np.where(data["Short_MA"] > data["Long_MA"], 1, 0)
    data["Position"] = data["Signal"].diff()
    return data

st.sidebar.subheader("Simple Moving Average (SMA) Trading Strategy")

# Input for selecting SMA windows
short_window = st.sidebar.slider("Select Short SMA Window Size:", 1, 50, 10)
long_window = st.sidebar.slider("Select Long SMA Window Size:", 50, 200, 50)

# Generate backtest data
strategy_data = sma_strategy(data.copy(), short_window, long_window)

# Plot the trading strategy
st.subheader(f"SMA Trading Strategy ({short_window}/{long_window}) for {ticker}")
plt.figure(figsize=(10, 5))
plt.plot(data.index, data["Close"], label="Price", alpha=0.7)
plt.plot(strategy_data.index, strategy_data["Short_MA"], label=f"Short SMA ({short_window})", alpha=0.7)
plt.plot(strategy_data.index, strategy_data["Long_MA"], label=f"Long SMA ({long_window})", alpha=0.7)
plt.fill_between(data.index, 0, 1, where=strategy_data["Signal"] == 1, color="green", alpha=0.2)
plt.fill_between(data.index, 0, 1, where=strategy_data["Signal"] == 0, color="red", alpha=0.2)
plt.legend()
plt.xlabel("Date")
plt.ylabel("Price")
st.pyplot()

fig, ax = plt.subplots()
ax.scatter([1, 2, 3], [1, 2, 3])

st.pyplot(fig)

# Buy/Sell signals
buy_signal = strategy_data["Position"].iloc[-1] > 0

st.sidebar.subheader("Buy/Sell Signal")
if buy_signal:
    st.markdown("<p style='font-size:20px;color:green;'>Buy Signal</p>", unsafe_allow_html=True)
else:
    st.markdown("<p style='font-size:20px;color:red;'>Sell Signal</p>", unsafe_allow_html=True)

# Note: For crypto analysis, you'd need a different data source and API.

# Closing note
st.write("This is a simplified example for demonstration purposes. Real trading strategies and predictions are much more complex and require advanced models and data analysis.")
