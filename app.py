import streamlit as st
import pandas as pd
import yfinance as yf
from streamlit_autorefresh import st_autorefresh

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Nifty 200 Losers Dashboard",
    layout="wide"
)

st_autorefresh(interval=30 * 1000, key="refresh")

st.title("📉 Nifty 200 Live Losers Dashboard")
st.markdown(
    f"**Last Updated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}"
)

# --------------------------------------------------
# FETCH NIFTY 200 LIST
# --------------------------------------------------
@st.cache_data
def get_nifty200_list():
    url = "https://archives.nseindia.com/content/indices/ind_nifty200list.csv"
    df = pd.read_csv(url)
    df["Ticker"] = df["Symbol"] + ".NS"
    return df

# --------------------------------------------------
# FETCH LIVE PRICES
# --------------------------------------------------
def fetch_live_prices(tickers):
    data = yf.download(
        tickers=tickers,
        period="1d",
        interval="1m",
        group_by="ticker",
        progress=False
    )

    prices = {}

    for ticker in tickers:
        try:
            price = data[ticker]["Close"].iloc[-1]
            prices[ticker] = round(float(price), 2)
        except Exception:
            prices[ticker] = None

    return prices

# --------------------------------------------------
# FETCH RETURNS
# --------------------------------------------------
def fetch_returns(tickers):
    data = yf.download(
        tickers=tickers,
        period="1mo",
        interval="1d",
        group_by="ticker",
        progress=False
    )

    returns = {}

    for ticker in tickers:
        try:
            close = data[ticker]["Close"].dropna()

            r1d = ((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2]) * 100
            r7d = ((close.iloc[-1] - close.iloc[-8]) / close.iloc[-8]) * 100 if len(close) >= 8 else None
            r1m = ((close.iloc[-1] - close.iloc[0]) / close.iloc[0]) * 100

            returns[ticker] = {
                "1D": round(r1d, 2),
                "7D": round(r7d, 2) if r7d is not None else None,
                "1M": round(r1m, 2)
            }

        except Exception:
            returns[ticker] = {
                "1D": None,
                "7D": None,
                "1M": None
            }

    return returns

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
df = get_nifty200_list()
tickers = df["Ticker"].tolist()

with st.spinner("Fetching live prices & returns..."):
    live_prices = fetch_live_prices(tickers)
    returns_data = fetch_returns(tickers)

df["Live Price (₹)"] = df["Ticker"].map(live_prices)
df["1D %"] = df["Ticker"].map(lambda x: returns_data[x]["1D"])
df["7D %"] = df["Ticker"].map(lambda x: returns_data[x]["7D"])
df["1M %"] = df["Ticker"].map(lambda x: returns_data[x]["1M"])

# --------------------------------------------------
# FILTER UI
# --------------------------------------------------
col1, col2 = st.columns([2, 1])

with col1:
    sector_filter = st.multiselect(
        "Sector Filter",
        options=sorted(df["Industry"].dropna().unique())
    )

with col2:
    loser_filter = st.selectbox(
        "Losers Period",
        ["None", "1 Day Losers", "7 Days Losers", "1 Month Losers"]
    )

# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------
df_display = df.copy()

if sector_filter:
    df_display = df_display[df_display["Industry"].isin(sector_filter)]

if loser_filter == "1 Day Losers":
    df_display = df_display[df_display["1D %"] < 0].sort_values("1D %")
elif loser_filter == "7 Days Losers":
    df_display = df_display[df_display["7D %"] < 0].sort_values("7D %")
elif loser_filter == "1 Month Losers":
    df_display = df_display[df_display["1M %"] < 0].sort_values("1M %")

# --------------------------------------------------
# DISPLAY TABLE
# --------------------------------------------------
columns = [
    "Symbol",
    "Company Name",
    "Industry",
    "Live Price (₹)",
    "1D %",
    "7D %",
    "1M %"
]

st.dataframe(
    df_display[columns].reset_index(drop=True),
    use_container_width=True,
    height=600
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.header("📊 Market Summary")
st.sidebar.metric("Total Stocks", len(df_display))
st.sidebar.info("Auto refresh every 30 seconds")

csv = df_display.to_csv(index=False).encode("utf-8")

st.sidebar.download_button(
    label="⬇ Download CSV",
    data=csv,
    file_name="nifty200_losers.csv",
    mime="text/csv"
)"NSE se list load nahi ho saki.")
