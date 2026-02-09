import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Nifty 200 Live Dashboard", layout="wide")

st.title("🚀 Nifty 200 Live Stock Tracker")

@st.cache_data
def get_nifty200_symbols():
    url = "https://archives.nseindia.com/content/indices/ind_nifty200list.csv"
    df = pd.read_csv(url)
    # yfinance ke liye NSE stocks mein '.NS' jodna zaroori hai
    df['Ticker'] = df['Symbol'] + ".NS"
    return df

# Data loading
df_list = get_nifty200_symbols()

# Sidebar for selection
st.sidebar.header("Settings")
if st.sidebar.button('🔄 Refresh Data'):
    st.rerun()

# Sirf top 10 ya selected stocks ka live price dikhane ke liye (performance ke liye)
st.subheader("Live Market Overview")
selected_stocks = st.multiselect("Stocks Select Karein:", df_list['Symbol'].tolist(), default=df_list['Symbol'].head(10).tolist())

if selected_stocks:
    tickers = [s + ".NS" for s in selected_stocks]
    # yfinance se live data fetch karna
    data = yf.download(tickers, period="1d", interval="1m")['Close'].iloc[-1]
    
    # Displaying in columns
    cols = st.columns(4)
    for i, (symbol, price) in enumerate(data.items()):
        cols[i % 4].metric(label=symbol.replace(".NS", ""), value=f"₹{price:.2f}")

st.write("---")
st.subheader("Full Nifty 200 List")
st.dataframe(df_list[['Symbol', 'Company Name', 'Industry']], use_container_width=True)
