import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Nifty 200 Live Professional Screener", layout="wide")
st.title("📊 Nifty 200 Live Advanced Screener")

# ======================================================
# NIFTY 200 SYMBOLS LIST
# ======================================================
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
    "UNIONBANK.NS", "UNITDSPR.NS", "UPL.NS", "VBL.NS", "VEDL.NS", "VOLTAS.NS", "WHIRLPOOL.NS", "WIPRO.NS", "YESBANK.NS", "ZEEL.NS", "ZOMATO.NS", "ZYDUSLIFE.NS"
]

# ======================================================
# LIVE DATA FETCHING (OPTIMIZED)
# ======================================================
@st.cache_data(ttl=300) # Refresh every 5 mins
def get_live_data(tickers):
    # Batch download to save time
    data = yf.download(tickers, period="2d", interval="1d", group_by='ticker', progress=False)
    
    final_list = []
    for ticker in tickers:
        try:
            hist = data[ticker]
            current_price = hist['Close'].iloc[-1]
            prev_close = hist['Close'].iloc[-2]
            volume = hist['Volume'].iloc[-1]
            
            change = current_price - prev_close
            p_change = (change / prev_close) * 100
            
            # Simple RSI Calculation for demo (Technical)
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs.iloc[-1]))

            final_list.append({
                "Symbol": ticker.replace(".NS", ""),
                "Price": round(current_price, 2),
                "Change": round(change, 2),
                "Change %": round(p_change, 2),
                "Volume": int(volume),
                "RSI (14)": round(rsi, 2) if not pd.isna(rsi) else 50,
                "MA Trend": "Above MA" if current_price > hist['Close'].rolling(20).mean().iloc[-1] else "Below MA"
            })
        except:
            continue
    return pd.DataFrame(final_list)

# Load Data
with st.spinner("Fetching Live Nifty 200 Data..."):
    df = get_live_data(nifty_200_tickers)

# ======================================================
# SIDEBAR FILTERS (Fixed for Live Data)
# ======================================================
st.sidebar.header("🔍 Filters")

# ---------- STOCK TYPE ----------
with st.sidebar.expander("📌 Price Action", expanded=True):
    action = st.radio("Show:", ["All", "Gainer", "Loser"])

# ---------- TECHNICAL ----------
with st.sidebar.expander("📉 Technical Filters"):
    use_rsi = st.sidebar.checkbox("Filter by RSI")
    rsi_val = st.sidebar.slider("RSI Range", 0, 100, (30, 70))
    
    use_ma = st.sidebar.checkbox("Filter by MA Trend")
    ma_choice = st.sidebar.selectbox("Condition", ["Above MA", "Below MA"])

# ======================================================
# APPLY FILTERS
# ======================================================
filtered_df = df.copy()

if action == "Gainer":
    filtered_df = filtered_df[filtered_df["Change %"] > 0]
elif action == "Loser":
    filtered_df = filtered_df[filtered_df["Change %"] < 0]

if use_rsi:
    filtered_df = filtered_df[filtered_df["RSI (14)"].between(rsi_val[0], rsi_val[1])]

if use_ma:
    filtered_df = filtered_df[filtered_df["MA Trend"] == ma_choice]

# ======================================================
# DISPLAY
# ======================================================
st.subheader(f"📄 Live Stocks ({len(filtered_df)})")

# Simple Styling for better look
def color_change(val):
    color = 'green' if val > 0 else 'red'
    return f'color: {color}'

st.dataframe(
    filtered_df.style.applymap(color_change, subset=['Change', 'Change %']),
    use_container_width=True,
    hide_index=True
)

st.info("💡 Tip: Fundamental data (ROE, P/E) takes longer to fetch for 200 stocks via free APIs. Use paid API like Dhan/Upstox for real-time fundamental screening.")
