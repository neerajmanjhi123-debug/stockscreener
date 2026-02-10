import streamlit as st
import pandas as pd
import yfinance as yf
from streamlit_autorefresh import st_autorefresh

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Nifty 200 Losers Dashboard", layout="wide")

st_autorefresh(interval=30 * 1000, key="refresh")

st.title("📉 Nifty 200 Live Losers Dashboard")
st.markdown(f"**Last Updated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

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
        tickers,
        period="1d",
        interval="1m",
        group_by="ticker",
        progress=False
    )

    prices = {}
    for ticker in tickers:
        try:
            prices[ticker] = round(data[ticker]["Close"].iloc[-1], 2)
        except:
            prices[ticker] = None
    return prices

# --------------------------------------------------
# FETCH RETURNS (1D / 7D / 1M)
# --------------------------------------------------
def fetch_returns(tickers):
    data = yf.download(
        tickers,
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
        except:
            returns[ticker] = {"1D": None, "7D": None, "1M": None}

    return returns

# --------------------------------------------------
# MAIN LOGIC
# --------------------------------------------------
df = get_nifty200_list()
tickers = df["Ticker"].tolist()

with st.spinner("Fetching Live Prices & Returns..."):
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
        options=sorted(df["Industry"].unique())
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
display_cols = [
    "Symbol",
    "Company Name",
    "Industry",
    "Live Price (₹)",
    "1D %",
    "7D %",
    "1M %"
]

st.dataframe(
    df_display[display_cols].reset_index(drop=True),
    use_container_width=True,
    height=600
)

# --------------------------------------------------
# SIDEBAR SUMMARY
# --------------------------------------------------
st.sidebar.header("📊 Market Summary")
st.sidebar.metric("Total Stocks", len(df_display))
st.sidebar.info("Auto refresh every 30 seconds")

csv = df_display.to_csv(index=False).encode("utf-8")
st.sidebar.download_button(
    "⬇ Download CSV",
    csv,
    "nifty200_losers.csv",
    "text/csv"
)            current_price = data[ticker]['Close'].iloc[-1]
            price_dict[ticker] = round(current_price, 2)
        except:
            price_dict[ticker] = "N/A"
    return price_dict

# --- Main Logic ---

df_stocks = get_nifty200_list()

if df_stocks is not None:
    with st.spinner('Fetching Live Prices...'):
        # Sirf tickers ki list nikal kar prices fetch karna
        tickers_list = df_stocks['Ticker'].tolist()
        live_prices = fetch_live_prices(tickers_list)
        
        # DataFrame mein prices add karna
        df_stocks['Live Price (₹)'] = df_stocks['Ticker'].map(live_prices)

    # 5. UI Layout - Filters
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_sector = st.multiselect("Sector Filter:", options=df_stocks['Industry'].unique())
    
    # Filter Logic
    if selected_sector:
        df_display = df_stocks[df_stocks['Industry'].isin(selected_sector)]
    else:
        df_display = df_stocks

    # 6. Display Data Table
    # Re-arranging columns for better view
    display_cols = ['Symbol', 'Company Name', 'Industry', 'Live Price (₹)']
    
    st.dataframe(
        df_display[display_cols].reset_index(drop=True), 
        use_container_width=True,
        height=600
    )

    # 7. Summary Stats
    st.sidebar.header("Market Summary")
    st.sidebar.metric("Total Stocks", len(df_stocks))
    st.sidebar.info("Dashboard 30 seconds mein auto-refresh ho raha hai.")
    
    # Download Link
    csv = df_display.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button("Download CSV", csv, "nifty200_live.csv", "text/csv")

else:
    st.error("NSE se list load nahi ho saki.")
