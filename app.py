import streamlit as st
import pandas as pd
from nifty200_list import nifty200_tickers

st.set_page_config(page_title="NIFTY 200 Stock Screener", layout="wide")

st.title("📊 NIFTY 200 Stocks Screener")
st.write("Below is the list of all NIFTY 200 stock tickers (NSE).")

# Convert list to pandas DataFrame
df = pd.DataFrame({"Ticker": nifty200_tickers})

# Show the table in Streamlit
st.dataframe(df)
