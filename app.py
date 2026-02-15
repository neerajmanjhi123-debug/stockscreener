==============================
st.sidebar.header("🔍 Filters")

show_fundamental_cols = st.sidebar.checkbox("Show Fundamental Columns")
show_technical_cols = st.sidebar.checkbox("Show Technical Columns")

# ---------- STOCK TYPE ----------
with st.sidebar.expander("📌 Stock Type", expanded=True):
    show_all = st.checkbox("All Stocks", True)
    gainer = st.checkbox("Gainer")
    loser = st.checkbox("Loser")

# ---------- VOLUME ----------
with st.sidebar.expander("📊 Volume"):
    high_vol = st.checkbox("High Volume")
    low_vol = st.checkbox("Low Volume")

# ---------- TIMEFRAME ----------
with st.sidebar.expander("⏱ Timeframe"):
    timeframe = st.multiselect(
        "Select Timeframe",
        ["Intraday", "Swing", "Positional", "Long Term"],
        default=["Swing"]
    )

# ---------- FUNDAMENTAL ----------
with st.sidebar.expander("🏦 Fundamental Filters"):
    use_roe = st.checkbox("ROE (%)")
    roe = st.slider("ROE Range", 0, 50, (15, 25))

    use_roce = st.checkbox("ROCE (%)")
    roce = st.slider("ROCE Min", 0, 50, 15)

    use_de = st.checkbox("Debt-to-Equity")
    de = st.slider("D/E Range", 0.0, 2.0, (0.0, 0.5))

# ---------- TECHNICAL ----------
with st.sidebar.expander("📉 Technical Filters"):
    use_rsi = st.checkbox("RSI (14)")
    rsi = st.slider("RSI Range", 0, 100, (40, 70))

    use_ma = st.checkbox("Price vs MA")
    ma_trend = st.selectbox("MA Condition", ["Above MA", "Below MA"])

# ======================================================
# APPLY FILTERS
# ======================================================
filtered_df = df.copy()

if not show_all:
    if gainer:
        filtered_df = filtered_df[filtered_df["Change %"] > 0]
    if loser:
        filtered_df = filtered_df[filtered_df["Change %"] < 0]

if high_vol:
    filtered_df = filtered_df[filtered_df["Volume"] > filtered_df["Volume"].median()]

if low_vol:
    filtered_df = filtered_df[filtered_df["Volume"] < filtered_df["Volume"].median()]

if use_roe:
    filtered_df = filtered_df[filtered_df["ROE (%)"].between(*roe)]

if use_roce:
    filtered_df = filtered_df[filtered_df["ROCE (%)"] >= roce]

if use_de:
    filtered_df = filtered_df[filtered_df["Debt-to-Equity"].between(*de)]

if use_rsi:
    filtered_df = filtered_df[filtered_df["RSI (14)"].between(*rsi)]

if use_ma:
    filtered_df = filtered_df[filtered_df["MA Trend"] == ma_trend]

# ======================================================
# DISPLAY LOGIC
# ======================================================
base_cols = [
    "S.No", "Symbol", "Stock Name",
    "Price", "Change", "Change %",
    "Sector"
]

fundamental_cols = [
    "ROE (%)", "ROCE (%)", "Debt-to-Equity",
    "Promoter Holding (%)", "Stock PE", "Sector PE",
    "Sales / Profit Growth (%)", "Interest Coverage Ratio",
    "Dividend Yield (%)"
]

technical_cols = ["RSI (14)", "MA Trend", "Volume"]

display_cols = base_cols.copy()

if show_fundamental_cols:
    display_cols.extend(fundamental_cols)

if show_technical_cols:
    display_cols.extend(technical_cols)

# ======================================================
# OUTPUT
# ======================================================
st.subheader("📄 Stock List")
st.dataframe(
    filtered_df[display_cols],
    use_container_width=True,
    hide_index=True
)

st.success("✅ Code fixed | No syntax error | All features preserved")
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Advanced Stock Screener", layout="wide")

st.title("📊 Advanced Stock Screener (Demo Version)")

# --------------------------------------------------
# DEMO STOCK DATA (5 Stocks)
# --------------------------------------------------
data = [
    {
        "Symbol": "RELIANCE",
        "Stock Name": "Reliance Industries",
        "Price": 2850.50,
        "Change": 25.40,
        "Percent Change": 0.90,
        "Sector": "Energy",
        "Volume": 5200000,
        "ROE (%)": 18,
        "ROCE (%)": 20,
        "Debt-to-Equity": 0.35,
        "Promoter Holding (%)": 50.6,
        "Pledged Shares (%)": 0,
        "Sales Growth (%)": 15,
        "Profit Growth (%)": 14,
        "Interest Coverage": 6,
        "Dividend Yield (%)": 1.2,
        "Upper BB": True,
        "Lower BB": False
    },
    {
        "Symbol": "TCS",
        "Stock Name": "Tata Consultancy Services",
        "Price": 3920.10,
        "Change": -40.20,
        "Percent Change": -1.02,
        "Sector": "IT",
        "Volume": 2100000,
        "ROE (%)": 42,
        "ROCE (%)": 45,
        "Debt-to-Equity": 0.05,
        "Promoter Holding (%)": 72,
        "Pledged Shares (%)": 0,
        "Sales Growth (%)": 12,
        "Profit Growth (%)": 13,
        "Interest Coverage": 20,
        "Dividend Yield (%)": 2.1,
        "Upper BB": False,
        "Lower BB": True
    },
    {
        "Symbol": "INFY",
        "Stock Name": "Infosys",
        "Price": 1580.00,
        "Change": 18.25,
        "Percent Change": 1.17,
        "Sector": "IT",
        "Volume": 3400000,
        "ROE (%)": 30,
        "ROCE (%)": 32,
        "Debt-to-Equity": 0.0,
        "Promoter Holding (%)": 13,
        "Pledged Shares (%)": 0,
        "Sales Growth (%)": 10,
        "Profit Growth (%)": 11,
        "Interest Coverage": 15,
        "Dividend Yield (%)": 2.5,
        "Upper BB": True,
        "Lower BB": False
    },
    {
        "Symbol": "ICICIBANK",
        "Stock Name": "ICICI Bank",
        "Price": 1045.80,
        "Change": -8.10,
        "Percent Change": -0.77,
        "Sector": "Banking",
        "Volume": 6100000,
        "ROE (%)": 16,
        "ROCE (%)": 18,
        "Debt-to-Equity": 0.45,
        "Promoter Holding (%)": 0,
        "Pledged Shares (%)": 0,
        "Sales Growth (%)": 19,
        "Profit Growth (%)": 22,
        "Interest Coverage": 4,
        "Dividend Yield (%)": 1.0,
        "Upper BB": False,
        "Lower BB": False
    },
    {
        "Symbol": "HDFCBANK",
        "Stock Name": "HDFC Bank",
        "Price": 1460.60,
        "Change": 12.80,
        "Percent Change": 0.88,
        "Sector": "Banking",
        "Volume": 4800000,
        "ROE (%)": 17,
        "ROCE (%)": 19,
        "Debt-to-Equity": 0.4,
        "Promoter Holding (%)": 25,
        "Pledged Shares (%)": 0,
        "Sales Growth (%)": 14,
        "Profit Growth (%)": 16,
        "Interest Coverage": 5,
        "Dividend Yield (%)": 1.3,
        "Upper BB": True,
        "Lower BB": False
    },
]

df = pd.DataFrame(data)

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.header("🔍 Filters")

# -------- Price Action --------
st.sidebar.subheader("Price Action")
all_stock = st.sidebar.checkbox("All Stocks", True)
gainer = st.sidebar.checkbox("Gainer")
loser = st.sidebar.checkbox("Loser")

# -------- Volume Filter --------
st.sidebar.subheader("Volume")
high_volume = st.sidebar.checkbox("High Volume")
low_volume = st.sidebar.checkbox("Low Volume")

# -------- Technical Filters --------
st.sidebar.subheader("Technical")
upper_bb = st.sidebar.checkbox("Upper Bollinger Band")
lower_bb = st.sidebar.checkbox("Lower Bollinger Band")

# -------- Fundamental Filters --------
st.sidebar.subheader("Fundamental (Tick to Apply)")

roe_filter = st.sidebar.checkbox("ROE 15% - 25%")
roce_filter = st.sidebar.checkbox("ROCE > 15%")
de_filter = st.sidebar.checkbox("Debt-to-Equity 0 - 0.5")
promoter_filter = st.sidebar.checkbox("Promoter Holding 50% - 75%")
pledge_filter = st.sidebar.checkbox("Pledged Shares = 0")
growth_filter = st.sidebar.checkbox("Sales & Profit Growth 10% - 20% (3Y)")
interest_filter = st.sidebar.checkbox("Interest Coverage > 3")
dividend_filter = st.sidebar.checkbox("Dividend Yield 1% - 3%")

# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------
filtered_df = df.copy()

if not all_stock:
    if gainer:
        filtered_df = filtered_df[filtered_df["Percent Change"] > 0]
    if loser:
        filtered_df = filtered_df[filtered_df["Percent Change"] < 0]

if high_volume:
    filtered_df = filtered_df[filtered_df["Volume"] > filtered_df["Volume"].mean()]

if low_volume:
    filtered_df = filtered_df[filtered_df["Volume"] < filtered_df["Volume"].mean()]

if upper_bb:
    filtered_df = filtered_df[filtered_df["Upper BB"] == True]

if lower_bb:
    filtered_df = filtered_df[filtered_df["Lower BB"] == True]

if roe_filter:
    filtered_df = filtered_df[(filtered_df["ROE (%)"] >= 15) & (filtered_df["ROE (%)"] <= 25)]

if roce_filter:
    filtered_df = filtered_df[filtered_df["ROCE (%)"] > 15]

if de_filter:
    filtered_df = filtered_df[(filtered_df["Debt-to-Equity"] >= 0) & (filtered_df["Debt-to-Equity"] <= 0.5)]

if promoter_filter:
    filtered_df = filtered_df[(filtered_df["Promoter Holding (%)"] >= 50) & (filtered_df["Promoter Holding (%)"] <= 75)]

if pledge_filter:
    filtered_df = filtered_df[filtered_df["Pledged Shares (%)"] == 0]

if growth_filter:
    filtered_df = filtered_df[
        (filtered_df["Sales Growth (%)"] >= 10) &
        (filtered_df["Profit Growth (%)"] >= 10)
    ]

if interest_filter:
    filtered_df = filtered_df[filtered_df["Interest Coverage"] > 3]

if dividend_filter:
    filtered_df = filtered_df[
        (filtered_df["Dividend Yield (%)"] >= 1) &
        (filtered_df["Dividend Yield (%)"] <= 3)
    ]

# --------------------------------------------------
# FINAL DISPLAY (ONLY MAIN COLUMNS)
# --------------------------------------------------
st.subheader("📋 Stock List")

display_df = filtered_df[[
    "Symbol",
    "Stock Name",
    "Price",
    "Change",
    "Percent Change",
    "Sector"
]]

display_df["Price"] = display_df["Price"].map(lambda x: f"{x:.2f}")
display_df["Change"] = display_df["Change"].map(lambda x: f"{x:.2f}")
display_df["Percent Change"] = display_df["Percent Change"].map(lambda x: f"{x:.2f}")

display_df.index = np.arange(1, len(display_df) + 1)

st.dataframe(display_df, use_container_width=True)
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
