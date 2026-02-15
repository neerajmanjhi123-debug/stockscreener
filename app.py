import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.set_page_config("NIFTY 200 Screener", layout="wide")

# =====================================================
# LOAD STOCK LIST FROM GITHUB
# =====================================================
@st.cache_data(ttl=300)
def load_universe():
    url = "https://raw.githubusercontent.com/yourname/nifty-universe/main/nifty200.csv"
    return pd.read_csv(url)

# =====================================================
# LOAD LIVE PRICE (Near realtime)
# =====================================================
@st.cache_data(ttl=300)
def load_price(symbols):
    symbols = [s + ".NS" for s in symbols]
    data = yf.download(symbols, period="1d", interval="5m", group_by="ticker")
    rows = []

    for s in symbols:
        try:
            close = data[s]["Close"].iloc[-1]
            prev = data[s]["Close"].iloc[-2]
            rows.append([s.replace(".NS",""), close, close-prev, (close-prev)/prev*100])
        except:
            pass

    return pd.DataFrame(rows, columns=["Symbol","Price","Change","Change %"])

# =====================================================
# DATA PREP
# =====================================================
df = load_universe()
price_df = load_price(df["Symbol"].tolist())
df = df.merge(price_df, on="Symbol", how="left")

df.insert(0,"S.No",range(1,len(df)+1))
df["Volume"] = np.random.randint(100000,5000000,len(df))
df["RSI"] = np.random.randint(30,80,len(df))
df["ROE (%)"] = np.random.randint(5,35,len(df))
df["Debt-to-Equity"] = np.round(np.random.uniform(0,1,len(df)),2)
df["Unusual Volume"] = np.where(df["Volume"] > df["Volume"].median()*1.5,"YES","NO")

# =====================================================
# CONDITIONS BUTTON
# =====================================================
if st.button("📌 Conditions"):
    st.info("Filters applied on LEFT side")

# =====================================================
# LAYOUT
# =====================================================
left, right = st.columns([1,3])

# =====================================================
# LEFT FILTERS
# =====================================================
with left:
    st.subheader("🔍 Filters")

    show_tech = st.checkbox("Show Technical Columns", True)
    show_fund = st.checkbox("Show Fundamental Columns", True)

    # ---------- STOCK TYPE ----------
    st.markdown("### Stock Type")
    gainer = st.checkbox("Gainer")
    loser = st.checkbox("Loser")

    # ---------- GAP ----------
    st.markdown("### Gap Filter")
    use_gap = st.checkbox("Apply Gap")
    gap_pct = st.number_input("Gap %", value=1.0)

    # ---------- VOLUME ----------
    st.markdown("### Volume")
    unusual = st.checkbox("Unusual Volume Only")

    # ---------- TIMEFRAME ----------
    st.markdown("### Timeframe")
    tf = st.selectbox("Type",["Minute","Hour","Day","Week","Month"])
    tf_val = st.number_input("Value",1)

    # ---------- FUNDAMENTAL ----------
    st.markdown("### Fundamental")
    use_roe = st.checkbox("ROE Filter")
    roe = st.slider("ROE %",0,50,(15,20))

    # ---------- TECHNICAL ----------
    st.markdown("### Technical")
    use_rsi = st.checkbox("RSI Filter")
    rsi = st.slider("RSI",0,100,(40,70))

# =====================================================
# APPLY FILTERS
# =====================================================
filtered = df.copy()

if gainer:
    filtered = filtered[filtered["Change %"] > 0]

if loser:
    filtered = filtered[filtered["Change %"] < 0]

if use_gap:
    filtered = filtered[filtered["Change %"].abs() >= gap_pct]

if unusual:
    filtered = filtered[filtered["Unusual Volume"] == "YES"]

if use_roe:
    filtered = filtered[filtered["ROE (%)"].between(*roe)]

if use_rsi:
    filtered = filtered[filtered["RSI"].between(*rsi)]

# =====================================================
# RIGHT SIDE LIST
# =====================================================
with right:
    st.subheader("📄 Stock List")

    cols = ["S.No","Symbol","Stock Name","Sector","Price","Change","Change %"]
    if show_tech:
        cols += ["RSI","Volume","Unusual Volume"]
    if show_fund:
        cols += ["ROE (%)","Debt-to-Equity"]

    st.dataframe(filtered[cols], use_container_width=True)

    # =================================================
    # STOCK CHART
    # =================================================
    st.subheader("📈 Chart")
    selected = st.selectbox("Select Stock", filtered["Symbol"].unique())

    indicators = st.multiselect("Indicators",["RSI","BB","EMA"])

    if selected:
        st.markdown(
            f"""
            <iframe src="https://www.tradingview.com/embed-widget/advanced-chart/?symbol=NSE:{selected}&interval=D&theme=light"
            width="100%" height="500"></iframe>
            """,
            unsafe_allow_html=True
        )# --------------------------------------------------
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
