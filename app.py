import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Nifty 500 Multi-Screener", layout="wide")
st.title("🚀 Nifty 500 Live Multi-Filter Screener")

# --------------------------------------------------
# NIFTY 500 TICKERS FETCHING
# --------------------------------------------------
@st.cache_data
def get_nifty_500_tickers():
    # Wikipedia ya official source se list fetch karna sabse sahi rehta hai
    # Demo ke liye hum top 500 symbols ka logic use kar rahe hain
    try:
        url = 'https://archives.nseindia.com/content/indices/ind_nifty500list.csv'
        df_sym = pd.read_csv(url)
        return [s + ".NS" for s in df_sym['Symbol'].tolist()]
    except:
        return ["RELIANCE.NS", "TCS.NS", "INFY.NS", "ZOMATO.NS", "TATAMOTORS.NS"] # Fallback

tickers = get_nifty_500_tickers()

# --------------------------------------------------
# LIVE DATA FETCHING
# --------------------------------------------------
@st.cache_data(ttl=60)
def fetch_nifty_500(ticker_list):
    # Batch download (Speed optimization)
    data = yf.download(ticker_list, period="2d", interval="1d", group_by='ticker', progress=False)
    
    rows = []
    for ticker in ticker_list:
        try:
            s_data = data[ticker].dropna()
            if len(s_data) < 2: continue
            
            curr = s_data['Close'].iloc[-1]
            prev = s_data['Close'].iloc[-2]
            open_p = s_data['Open'].iloc[-1]
            
            change = curr - prev
            p_change = (change / prev) * 100
            gap = ((open_p - prev) / prev) * 100

            rows.append({
                "Symbol": ticker.replace(".NS", ""),
                "Price": curr,
                "Change": change,
                "Percent Change": p_change,
                "Gap %": gap
            })
        except:
            continue
    return pd.DataFrame(rows)

# Load Data
with st.spinner(f"Fetching {len(tickers)} Stocks... Please wait."):
    df = fetch_nifty_500(tickers)

# --------------------------------------------------
# SIDEBAR MULTI-FILTERS (TICK BOXES)
# --------------------------------------------------
st.sidebar.header("🔍 Select Multiple Filters")

# Tick boxes (Checkboxes)
f_gainer = st.sidebar.checkbox("🟢 Gainers (>0%)")
f_loser = st.sidebar.checkbox("🔴 Losers (<0%)")
f_gap_up = st.sidebar.checkbox("⬆️ Gap Up (>0.5%)")
f_gap_down = st.sidebar.checkbox("⬇️ Gap Down (<-0.5%)")

# Apply Logic (AND condition agar multiple select hain)
filtered_df = df.copy()

if f_gainer:
    filtered_df = filtered_df[filtered_df["Percent Change"] > 0]
if f_loser:
    filtered_df = filtered_df[filtered_df["Percent Change"] < 0]
if f_gap_up:
    filtered_df = filtered_df[filtered_df["Gap %"] > 0.5]
if f_gap_down:
    filtered_df = filtered_df[filtered_df["Gap %"] < -0.5]

# Search Box
search = st.sidebar.text_input("Search Symbol (e.g. TATA)")
if search:
    filtered_df = filtered_df[filtered_df["Symbol"].str.contains(search.upper())]

# --------------------------------------------------
# FORMATTING & DISPLAY
# --------------------------------------------------
st.subheader(f"📊 Results: {len(filtered_df)} Stocks Found")

# Formatting to .00
display_df = filtered_df.copy()
display_df["Price"] = display_df["Price"].apply(lambda x: f"{x:,.2f}")
display_df["Change"] = display_df["Change"].apply(lambda x: f"{x:,.2f}")
display_df["Percent Change"] = display_df["Percent Change"].apply(lambda x: f"{x:.2f}%")
display_df["Gap %"] = display_df["Gap %"].apply(lambda x: f"{x:.2f}%")

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    height=600
)

# Refresh Button
if st.button("🔄 Refresh Market Data"):
    st.cache_data.clear()
    st.rerun()
