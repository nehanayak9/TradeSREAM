import yfinance as yf
import streamlit as st
from PIL import Image
from urllib.request import urlopen

#Title and subtiles
st.title("Cryptocurrency Daily Prices")
st.header("Main Dashboard")
st.subheader("you can add more crypto in code")


#Defining ticker variables
Bitcoin = "BTC-USD"
Ethereum = "ETH-USD"
Ripple = "XRP-USD"
BitcoinCash = "BCH-USD"

#Acess data from Yahaoo Finance 
BTC_Data = yf.Ticker(Bitcoin)
ETH_Data = yf.Ticker(Ethereum)
XRP_Data = yf.Ticker(Ripple)
BCH_Data = yf.Ticker(BitcoinCash)

#Fetch history data from Yahoo Finance 
BTCHis = BTC_Data.history(period="max")
ETHHis = ETH_Data.history(period="max")
XRPHis = XRP_Data.history(period="max")
BCHHis = BCH_Data.history(period="max")

#Fetch crypto data for the dataframe
BTC = yf.download(Bitcoin, start="2023-11-18",end ="2023-11-18")
ETH = yf.download(Ethereum, start="2023-11-18",end ="2023-11-18")
XRP = yf.download(Ripple, start="2023-11-18",end ="2023-11-18")
BCH = yf.download(BitcoinCash, start="2023-11-18",end ="2023-11-18") 

#Bitcoin
st.write("Bitcoin ($)")
imageBTC = Image.open(urlopen("https://s2.coinmarketcap.com/static/img/coins/64x64/1.png"))
#Display image
st.image(imageBTC)
#Display dataframe
st.table(BTC)
#Display a chart
st.bar_chart(BTCHis.Close)


#Ethereum
st.write("Etherem ($)")
imageETH = Image.open(urlopen("https://s2.coinmarketcap.com/static/img/coins/64x64/1027.png"))
#Display image
st.image(imageETH)
#Display dataframe
st.table(ETH)
#Display a chart
st.bar_chart(ETHHis.Close)


#Ripple
st.write("Ripple ($)")
imageXRP = Image.open(urlopen("https://s2.coinmarketcap.com/static/img/coins/64x64/52.png"))
#Display image
st.image(imageXRP)
#Display dataframe
st.table(XRP)
#Display a chart
st.bar_chart(XRPHis.Close)

#BitcoinCash
st.write("BITCOIN CASH ($)")
imageBCH = Image.open(urlopen("https://s2.coinmarketcap.com/static/img/coins/64x64/1813.png"))
#Display image
st.image(imageBCH)
#Display dataframe
st.table(BCH)
#Display a chart
st.bar_chart(BCHHis.Close)