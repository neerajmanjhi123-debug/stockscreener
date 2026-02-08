import streamlit as st
import pandas as pd

# NIFTY 500 tickers list (partial example)
tickers = [
    "360ONE.NS","3MINDIA.NS","ABB.NS","ACC.NS","AIAENG.NS",
    "APLAPOLLO.NS","AUBANK.NS","AARTIIND.NS","AAVAS.NS",
    "ABBOTINDIA.NS","ADANIENT.NS","ADANIGREEN.NS","ADANIPORTS.NS"
    # ... (continue with full list available from gist)
]

# Dikhane ke liye pandas DataFrame
df = pd.DataFrame({"Ticker": tickers})

st.title("📈 NIFTY 500 Stocks List")
st.write("Below are the NIFTY 500 tickers loaded from GitHub gist:")

# Table show karo
st.dataframe(df)
