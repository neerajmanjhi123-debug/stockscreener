import streamlit as st
import pandas as pd
import numpy as np

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Stock Screener", layout="wide")
st.title("📊 Advanced Stock Screener (Demo – Stable Version)")

# ---------------- DEMO DATA ----------------
data = [
    ["RELIANCE", "Reliance Industries", 2850.50, 25.40, 0.90, "Energy", 5200000, 18, 20, 0.35, 50.6, 0, 15, 14, 6, 1.2, True, False],
    ["TCS", "Tata Consultancy Services", 3920.10, -40.20, -1.02, "IT", 2100000, 42, 45, 0.05, 72, 0, 12, 13, 20, 2.1, False, True],
    ["INFY", "Infosys", 1580.00, 18.25, 1.17, "IT", 3400000, 30, 32, 0.00, 13, 0, 10, 11, 15, 2.5, True, False],
    ["ICICIBANK", "ICICI Bank", 1045.80, -8.10, -0.77, "Banking", 6100000, 16, 18, 0.45, 0, 0, 19, 22, 4, 1.0, False, False],
    ["HDFCBANK", "HDFC Bank", 1460.60, 12.80, 0.88, "Banking", 4800000, 17, 19, 0.40, 25, 0, 14, 16, 5, 1.3, True, False],
]

columns = [
    "Symbol", "Stock Name", "Price", "Change", "Percent Change", "Sector",
    "Volume", "ROE (%)", "ROCE (%)", "Debt-to-Equity",
    "Promoter Holding (%)", "Pledged Shares (%)",
    "Sales Growth (%)", "Profit Growth (%)",
    "Interest Coverage", "Dividend Yield (%)",
    "Upper BB", "Lower BB"
]

df = pd.DataFrame(data, columns=columns)

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔍 Filters")

all_stock = st.sidebar.checkbox("All Stocks", True)
gainer = st.sidebar.checkbox("Gainer")
loser = st.sidebar.checkbox("Loser")

st.sidebar.subheader("Volume")
high_volume = st.sidebar.checkbox("High Volume")
low_volume = st.sidebar.checkbox("Low Volume")

st.sidebar.subheader("Technical")
upper_bb = st.sidebar.checkbox("Upper Bollinger Band")
lower_bb = st.sidebar.checkbox("Lower Bollinger Band")

st.sidebar.subheader("Fundamental")
roe = st.sidebar.checkbox("ROE 15–25%")
roce = st.sidebar.checkbox("ROCE > 15%")
de = st.sidebar.checkbox("Debt-to-Equity 0–0.5")
promoter = st.sidebar.checkbox("Promoter Holding 50–75%")
pledge = st.sidebar.checkbox("Pledged Shares = 0")
growth = st.sidebar.checkbox("Sales & Profit Growth ≥ 10%")
interest = st.sidebar.checkbox("Interest Coverage > 3")
dividend = st.sidebar.checkbox("Dividend Yield 1–3%")

# ---------------- APPLY FILTERS ----------------
fdf = df.copy()

if not all_stock:
    if gainer:
        fdf = fdf[fdf["Percent Change"] > 0]
    if loser:
        fdf = fdf[fdf["Percent Change"] < 0]

if high_volume:
    fdf = fdf[fdf["Volume"] > fdf["Volume"].mean()]

if low_volume:
    fdf = fdf[fdf["Volume"] < fdf["Volume"].mean()]

if upper_bb:
    fdf = fdf[fdf["Upper BB"] == True]

if lower_bb:
    fdf = fdf[fdf["Lower BB"] == True]

if roe:
    fdf = fdf[(fdf["ROE (%)"] >= 15) & (fdf["ROE (%)"] <= 25)]

if roce:
    fdf = fdf[fdf["ROCE (%)"] > 15]

if de:
    fdf = fdf[(fdf["Debt-to-Equity"] >= 0) & (fdf["Debt-to-Equity"] <= 0.5)]

if promoter:
    fdf = fdf[(fdf["Promoter Holding (%)"] >= 50) & (fdf["Promoter Holding (%)"] <= 75)]

if pledge:
    fdf = fdf[fdf["Pledged Shares (%)"] == 0]

if growth:
    fdf = fdf[(fdf["Sales Growth (%)"] >= 10) & (fdf["Profit Growth (%)"] >= 10)]

if interest:
    fdf = fdf[fdf["Interest Coverage"] > 3]

if dividend:
    fdf = fdf[(fdf["Dividend Yield (%)"] >= 1) & (fdf["Dividend Yield (%)"] <= 3)]

# ---------------- FINAL TABLE ----------------
st.subheader("📋 Stock List")

show_df = fdf[
    ["Symbol", "Stock Name", "Price", "Change", "Percent Change", "Sector"]
].copy()

show_df["Price"] = show_df["Price"].round(2)
show_df["Change"] = show_df["Change"].round(2)
show_df["Percent Change"] = show_df["Percent Change"].round(2)

show_df.index = np.arange(1, len(show_df) + 1)

st.dataframe(show_df, use_container_width=True)
