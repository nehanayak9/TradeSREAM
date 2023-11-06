import streamlit as st, pandas as pd, numpy as np
import plotly.express as px
import yfinance as yf
import pandas as pd
from urllib.request import urlopen


st.title('Stock Dashboard')
ticker = st.sidebar.text_input('Ticker')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

data = yf.download(ticker, start=start_date, end=end_date)

fig = px.line(data, x = data.index, y = data['Adj Close'], title = ticker)
st.plotly_chart(fig)

pricing_data, fundamental_data, news = st.tabs(["Pricing Data", "Fundamental Data", "Top 10 News"])

with pricing_data:
    data2 = data
    data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1)
    data2.dropna(inplace = True)
    st.write(data2)
    annual_return = data2['% Change'].mean()*252*100
    st.write('Annual Return is',annual_return,'%')
    stdev = np.std(data2['% Change'])*np.sqrt(252)
    st.write('Standard Deviation is',stdev*100,'%')
    st.write('Risk Adj. is',annual_return/(stdev*100))
    
with fundamental_data:
    st.write('Fundamental')
    
with news:
    st.write('News')