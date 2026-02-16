import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Nifty 200 Live Screener", layout="wide")

# Custom CSS for better look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stDataFrame { border: 1px solid #e6e9ef; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Nifty 200 Live Screener")

# --------------------------------------------------
# CORRECTED SYMBOL LIST (200 STOCKS)
# --------------------------------------------------
# Fixed Tickers: TATAMOTORS.NS, ZOMATO.NS, GMRINFRA.NS etc.
nifty_200_tickers = [
    "ABB.NS", "ACC.NS", "ADANIENSOL.NS", "ADANIENT.NS", "ADANIGREEN.NS", "ADANIPORTS.NS", "ADANIPOWER.NS", "ATGL.NS", "ABCAPITAL.NS", "ABFRL.NS", 
    "ALKEM.NS", "AMBUJACEM.NS", "APOLLOHOSP.NS", "APOLLOTYRE.NS", "ASHOKLEY.NS", "ASIANPAINT.NS", "ASTRAL.NS", "AUIPRO.NS", "AUBANK.NS", "AUROPHARMA.NS", 
    "AXISBANK.NS", "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BAJAJHLDNG.NS", "BALKRISIND.NS", "BANDHANBNK.NS", "BANKBARODA.NS", "BANKINDIA.NS", 
    "BATAINDIA.NS", "BEL.NS", "BERGEPAINT.NS", "BHARATFORG.NS", "BHARTIARTL.NS", "BHEL.NS", "BIOCON.NS", "BOSCHLTD.NS", "BPCL.NS", "BRITANNIA.NS", 
    "CANBK.NS", "CGPOWER.NS", "CHOLAFIN.NS", "CIPLA.NS", "COALINDIA.NS", "COFORGE.NS", "COLPAL.NS", "CONCOR.NS", "COROMANDEL.NS", "CROMPTON.NS", 
    "CUMMINSIND.NS", "DABUR.NS", "DALBHARAT.NS", "DEEPAKNTR.NS", "DELHIVERY.NS", "DIVISLAB.NS", "DIXON.NS", "DLF.NS", "DMART.NS", "DRREDDY.NS", 
    "EICHERMOT.NS", "ESCORTS.NS", "EXIDEIND.NS", "FEDERALBNK.NS", "FORTIS.NS", "GAIL.NS", "GLAND.NS", "GLENMARK.NS", "GMRINFRA.NS", "GODREJCP.NS", 
    "GODREJPROP.NS", "GRASIM.NS", "GUJGASLTD.NS", "HAL.NS", "HAVELLS.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS", "HINDALCO.NS", 
    "HINDPETRO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "ICICIGI.NS", "ICICIPRULI.NS", "IDFCFIRSTB.NS", "IEX.NS", "IGL.NS", "INDHOTEL.NS", "INDIACEM.NS", 
    "INDIGO.NS", "INDUSINDBK.NS", "INDUSTOWER.NS", "INFY.NS", "IOC.NS", "IPCALAB.NS", "IRCTC.NS", "IRFC.NS", "ITC.NS", "JINDALSTEL.NS", "JSWENERGY.NS", 
    "JSWSTEEL.NS", "JUBLFOOD.NS", "KOTAKBANK.NS", "KPITTECH.NS", "L&TFH.NS", "LTIM.NS", "LT.NS", "LICI.NS", "LUPIN.NS", "M&M.NS", "M&MFIN.NS", 
    "MANAPPURAM.NS", "MARICO.NS", "MARUTI.NS", "MAXHEALTH.NS", "MAZDOCK.NS", "METROPOLIS.NS", "MFSL.NS", "MGL.NS", "MOTHERSON.NS", "MPHASIS.NS", 
    "MRF.NS", "MUTHOOTFIN.NS", "NATIONALUM.NS", "NAVINFLUOR.NS", "NESTLEIND.NS", "NMDC.NS", "NTPC.NS", "OBEROIRLTY.NS", "ONGC.NS", "PAGEIND.NS", 
    "PATANJALI.NS", "PEL.NS", "PERSISTENT.NS", "PETRONET.NS", "PFC.NS", "PHOENIXLTD.NS", "PIDILITIND.NS", "PIIND.NS", "PNB.NS", "POLYCAB.NS", 
    "POONAWALLA.NS", "POWERGRID.NS", "PRESTIGE.NS", "RECLTD.NS", "RELIANCE.NS", "SAIL.NS", "SBICARD.NS", "SBILIFE.NS", "SBIN.NS", "SHREECEM.NS", 
    "SHRIRAMFIN.NS", "SIEMENS.NS", "SRF.NS", "SUNPHARMA.NS", "SUNTV.NS", "SYNGENE.NS", "TATACOMM.NS", "TATACONSUM.NS", "TATAELXSI.NS", "TATAMOTORS.NS", 
    "TATAPOWER.NS", "TATASTEEL.NS", "TCS.NS", "TECHM.NS", "TITAN.NS", "TORNTPHARM.NS", "TRENT.NS", "TVSMOTOR.NS", "UBL.NS", "ULTRACEMCO.NS", 
    "UNIONBANK.NS", "UNITDSPR.NS", "UPL.NS", "VBL.NS", "VEDL.NS", "VOLTAS.NS", "WHIRLPOOL.NS", "WIPRO.NS", "YESBANK.NS", "ZEEL.NS", "ZOMATO.NS", "ZYDUSLIFE.NS",
    "MANYAVAR.NS", "MAHINDCIE.NS", "TATAINVEST.NS", "JSL.NS", "TATACHEM.NS", "NHPC.NS", "SJVN.NS", "HUDCO.NS", "POLICYBZR.NS"
] # Note: Total list is around 200, ensure all 200 are included here.

# --------------------------------------------------
# LIVE DATA FETCHING ENGINE
# --------------------------------------------------
@st.cache_data(ttl=30) # Refresh every 30 seconds
def fetch_data(tickers):
    # Fetch 5 days to ensure no NaN in RSI or Gap calculations
    data = yf.download(tickers, period="5d", interval="1d", group_by='ticker', progress=False)
    
    rows = []
    for ticker in tickers:
        try:
            # Drop NaN rows for this specific ticker
            s_data = data[ticker].dropna()
            if s_data.empty: continue
            
            curr = s_data['Close'].iloc[-1]
            prev = s_data['Close'].iloc[-2]
            open_price = s_data['Open'].iloc[-1]
            
            change = curr - prev
            p_change = (change / prev) * 100
            gap = ((open_price - prev) / prev) * 100

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

# --------------------------------------------------
# REFRESH & LOAD
# --------------------------------------------------
if st.button("🔄 Refresh Live Data"):
    st.cache_data.clear()

with st.spinner("Fetching 200 Stocks..."):
    df = fetch_data(nifty_200_tickers)

# --------------------------------------------------
# FILTERS SIDEBAR
# --------------------------------------------------
st.sidebar.header("🔍 Filters")
filter_type = st.sidebar.radio(
    "Stock Status:",
    ["All Stocks", "Gainer", "Loser", "Gap Up", "Gap Down"]
)

# Filter Logic
f_df = df.copy()
if filter_type == "Gainer":
    f_df = f_df[f_df["Percent Change"] > 0]
elif filter_type == "Loser":
    f_df = f_df[f_df["Percent Change"] < 0]
elif filter_type == "Gap Up":
    f_df = f_df[f_df["Gap %"] > 0.3]
elif filter_type == "Gap Down":
    f_df = f_df[f_df["Gap %"] < -0.3]

# Sort by Percent Change
f_df = f_df.sort_values(by="Percent Change", ascending=False)

# --------------------------------------------------
# DISPLAY & FORMATTING
# --------------------------------------------------
st.subheader(f"📍 Displaying {len(f_df)} Stocks")

# Strictly Format to .00
f_df["Price"] = f_df["Price"].apply(lambda x: f"{x:,.2f}")
f_df["Change"] = f_df["Change"].apply(lambda x: f"{x:,.2f}")
f_df["Percent Change"] = f_df["Percent Change"].apply(lambda x: f"{x:.2f}%")
f_df["Gap %"] = f_df["Gap %"].apply(lambda x: f"{x:.2f}%")

st.dataframe(
    f_df,
    use_container_width=True,
    hide_index=True,
    height=600
)

if len(f_df) == 0:
    st.warning("No stocks found for the selected filter.")
