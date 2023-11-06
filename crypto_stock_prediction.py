import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set the title and subtitle
st.title("Crypto and Stock Price Analysis")
st.write("A Streamlit app for historical price display, analysis, and a basic trading strategy backtest.")

# Sidebar
st.sidebar.subheader("Select Stock/Crypto and Time Period")

# Input for selecting stock/crypto
ticker = st.sidebar.text_input("Enter Ticker Symbol (e.g., AAPL, BTC-USD):", "AAPL")

# Input for selecting date range
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2023-12-31"))

# Download historical data
data = yf.download(ticker, start=start_date, end=end_date)

# Display historical data
st.subheader(f"Historical {ticker} Data")
st.write(data)

# Interactive line chart
st.subheader(f"Interactive Price Chart for {ticker}")
st.line_chart(data["Close"])

# Simple Moving Average (SMA) prediction
def sma_prediction(data, window):
    data["SMA"] = data["Close"].rolling(window=window).mean()
    return data

st.sidebar.subheader("Simple Moving Average (SMA) Prediction")

# Input for selecting SMA window size
sma_window = st.sidebar.slider("Select SMA Window Size:", 1, 100, 20)

# Generate SMA data
sma_data = sma_prediction(data, sma_window)

# Display SMA prediction chart
st.subheader(f"SMA {sma_window} Prediction for {ticker}")
st.line_chart(sma_data[["Close", "SMA"]])

# Basic Analysis
st.sidebar.subheader("Basic Analysis")

# Calculate statistics
avg_close = data["Close"].mean()
min_close = data["Close"].min()
max_close = data["Close"].max()
st.write(f"Average {ticker} Closing Price: ${avg_close:.2f}")
st.write(f"Minimum {ticker} Closing Price: ${min_close:.2f}")
st.write(f"Maximum {ticker} Closing Price: ${max_close:.2f}")

# Trading Strategy Backtest
def backtest(data, short_window, long_window):
    data["Short_MA"] = data["Close"].rolling(window=short_window).mean()
    data["Long_MA"] = data["Close"].rolling(window=long_window).mean()
    data["Signal"] = np.where(data["Short_MA"] > data["Long_MA"], 1, 0)
    data["Position"] = data["Signal"].diff()
    return data

st.sidebar.subheader("Simple Moving Average (SMA) Trading Strategy Backtest")

# Input for selecting SMA windows
short_window = st.sidebar.slider("Select Short SMA Window Size:", 1, 50, 10)
long_window = st.sidebar.slider("Select Long SMA Window Size:", 50, 200, 50)

# Generate backtest data
backtest_data = backtest(data.copy(), short_window, long_window)

# Plot the trading strategy
st.subheader(f"SMA Trading Strategy ({short_window}/{long_window}) for {ticker}")
plt.figure(figsize=(10, 5))
plt.plot(data.index, data["Close"], label="Price", alpha=0.7)
plt.plot(backtest_data.index, backtest_data["Short_MA"], label=f"Short SMA ({short_window})", alpha=0.7)
plt.plot(backtest_data.index, backtest_data["Long_MA"], label=f"Long SMA ({long_window})", alpha=0.7)
plt.fill_between(data.index, 0, 1, where=backtest_data["Signal"] == 1, color="green", alpha=0.2)
plt.fill_between(data.index, 0, 1, where=backtest_data["Signal"] == 0, color="red", alpha=0.2)
plt.legend()
plt.xlabel("Date")
plt.ylabel("Price")
st.pyplot()

# Note: For crypto analysis, you'd need a different data source.
fig, ax = plt.subplots()
ax.scatter([1, 2, 3], [1, 2, 3])

st.pyplot(fig)

st.set_option('deprecation.showPyplotGlobalUse', False)

# Buy/Sell Prediction
buy_signal = backtest_data["Position"].iloc[-1] > 0

st.sidebar.subheader("Buy/Sell Prediction")
if buy_signal:
    st.write(f"Based on the SMA strategy, it's recommended to buy {ticker} at the last available data point.")
else:
    st.write(f"Based on the SMA strategy, it's recommended to sell {ticker} at the last available data point.")

# Closing note
st.write("This is a more graphical and informative example for demonstration purposes. Real analysis and trading strategies can be much more complex.")


