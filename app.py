import streamlit as st
import pandas as pd
from nifty200_list import nifty200_tickers

st.title("📊 NIFTY 200 Stocks List")

st.write("Below is the list of all NIFTY 200 stock tickers (NSE):")

# DataFrame banayein
df = pd.DataFrame({"Ticker": nifty200_tickers})

# Table show karein
st.dataframe(df)
