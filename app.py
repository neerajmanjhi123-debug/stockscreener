import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="NIFTY 200 Stock Screener", layout="wide")
st.title("📊 NIFTY 200 Stock Screener (Stable Version)")

# -------------------------------------------------
# NIFTY 200 STOCK SYMBOL LIST (Sample – Expandable)
# -------------------------------------------------
nifty_200_symbols = [
    "RELIANCE","TCS","INFY","HDFCBANK","ICICIBANK","ITC","LT","SBIN","AXISBANK",
    "BAJFINANCE","BAJAJFINSV","HINDUNILVR","KOTAKBANK","ADANIENT","ADANIPORTS",
    "ASIANPAINT","MARUTI","TITAN","ULTRACEMCO","SUNPHARMA","WIPRO","ONGC",
    "POWERGRID","NTPC","COALINDIA","TATASTEEL","JSWSTEEL","HCLTECH","DIVISLAB",
    "DRREDDY","EICHERMOT","BPCL","GRASIM","HEROMOTOCO","BRITANNIA","APOLLOHOSP"
]

# -------------------------------------------------
# CREATE DEMO DATA FOR ALL STOCKS
# -------------------------------------------------
rows = []
np.random.seed(1)

for sym in nifty_200_symbols:
    price = round(np.random.uniform(100, 3000), 2)
    change = round(np.random.uniform(-50, 50), 2)
    pct = round((change / price) * 100, 2)
    volume = np.random.randint(5_00_000, 80_00_000)

    rows.append([
        sym,
        sym + " Ltd",
        price,
        change,
        pct,
        "Sector",
        volume
    ])

df = pd.DataFrame(
    rows,
    columns=[
        "Symbol",
        "Stock Name",
        "Price",
        "Change",
        "Percent Change",
        "Sector",
        "Volume"
    ]
)

df.insert(0, "S.No", range(1, len(df) + 1))

# -------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------
st.sidebar.header("🔍 Filters")

all_stock = st.sidebar.checkbox("All Stocks", True)
gainer = st.sidebar.checkbox("Gainer")
loser = st.sidebar.checkbox("Loser")

high_vol = st.sidebar.checkbox("High Volume")
low_vol = st.sidebar.checkbox("Low Volume")

# -------------------------------------------------
# APPLY FILTERS
# -------------------------------------------------
fdf = df.copy()

if not all_stock:
    if gainer:
        fdf = fdf[fdf["Percent Change"] > 0]
    if loser:
        fdf = fdf[fdf["Percent Change"] < 0]

if high_vol:
    fdf = fdf[fdf["Volume"] > fdf["Volume"].median()]

if low_vol:
    fdf = fdf[fdf["Volume"] < fdf["Volume"].median()]

# -------------------------------------------------
# FINAL DISPLAY
# -------------------------------------------------
st.subheader(f"📋 NIFTY 200 Stock List ({len(fdf)} Stocks)")

show_df = fdf[
    ["S.No", "Symbol", "Stock Name", "Price", "Change", "Percent Change", "Sector"]
].copy()

show_df["Price"] = show_df["Price"].round(2)
show_df["Change"] = show_df["Change"].round(2)
show_df["Percent Change"] = show_df["Percent Change"].round(2)

st.dataframe(show_df, use_container_width=True)
