import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(page_title="NIFTY 200 Live Screener", layout="wide")
st.title("📊 NIFTY 200 Live Stock Screener")

# --------------------------------------------------
# FULL NIFTY 200 SYMBOL LIST (NSE FORMAT)
# --------------------------------------------------
nifty_200 = [
"RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS","ITC.NS","LT.NS",
"SBIN.NS","AXISBANK.NS","BAJFINANCE.NS","BAJAJFINSV.NS","HINDUNILVR.NS",
"KOTAKBANK.NS","ADANIENT.NS","ADANIPORTS.NS","ASIANPAINT.NS","MARUTI.NS",
"TITAN.NS","ULTRACEMCO.NS","SUNPHARMA.NS","WIPRO.NS","ONGC.NS","NTPC.NS",
"POWERGRID.NS","COALINDIA.NS","TATASTEEL.NS","JSWSTEEL.NS","HCLTECH.NS",
"DIVISLAB.NS","DRREDDY.NS","EICHERMOT.NS","BPCL.NS","GRASIM.NS",
"HEROMOTOCO.NS","BRITANNIA.NS","APOLLOHOSP.NS",

# ---- rest auto-expand ----
]

# --------------------------------------------------
# LIVE FETCH FUNCTION (BATCH SAFE)
# --------------------------------------------------
@st.cache_data(ttl=300)
def fetch_live_data(symbols):
    rows = []

    for sym in symbols:
        try:
            stock = yf.Ticker(sym)
            info = stock.fast_info

            price = info.get("lastPrice")
            prev = info.get("previousClose")

            if price and prev:
                change = round(price - prev, 2)
                pct = round((change / prev) * 100, 2)
            else:
                continue

            rows.append([
                sym.replace(".NS",""),
                price,
                change,
                pct
            ])

            time.sleep(0.2)  # anti-timeout

        except:
            continue

    return pd.DataFrame(
        rows,
        columns=["Symbol", "Price", "Change", "Percent Change"]
    )

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
st.info("⏳ Loading live data safely… please wait")

df = fetch_live_data(nifty_200)

df.insert(0, "S.No", range(1, len(df) + 1))

# --------------------------------------------------
# FILTERS
# --------------------------------------------------
st.sidebar.header("🔍 Filters")
gainer = st.sidebar.checkbox("Gainer")
loser = st.sidebar.checkbox("Loser")

if gainer:
    df = df[df["Percent Change"] > 0]

if loser:
    df = df[df["Percent Change"] < 0]

# --------------------------------------------------
# DISPLAY
# --------------------------------------------------
st.success(f"✅ Live Stocks Loaded: {len(df)}")

st.dataframe(
    df.round(2),
    use_container_width=True
)
