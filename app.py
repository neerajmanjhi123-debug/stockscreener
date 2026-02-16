import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="NIFTY 200 Live Screener", layout="wide")
st.title("📊 NIFTY 200 Live Stock Screener")

# --------------------------------------------------
# NIFTY 200 SYMBOLS LIST
# --------------------------------------------------
nifty_200_symbols = [
    "ABB.NS", "ACC.NS", "ADANIENSOL.NS", "ADANIENT.NS", "ADANIGREEN.NS", "ADANIPORTS.NS", "ADANIPOWER.NS", "ATGL.NS", "ABCAPITAL.NS", "ABFRL.NS", 
    "ALKEM.NS", "AMBUJACEM.NS", "APOLLOHOSP.NS", "APOLLOTYRE.NS", "ASHOKLEY.NS", "ASIANPAINT.NS", "ASTRAL.NS", "AUIPRO.NS", "AUBANK.NS", "AUROPHARMA.NS", 
    "AVANTIFEED.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BAJAJHLDNG.NS", "BALKRISIND.NS", "BANDHANBNK.NS", "BANKBARODA.NS", "BANKINDIA.NS", 
    "BATAINDIA.NS", "BEL.NS", "BERGEPAINT.NS", "BHARATFORG.NS", "BHARTIARTL.NS", "BHEL.NS", "BIOCON.NS", "BOSCHLTD.NS", "BPCL.NS", "BRITANNIA.NS", 
    "BSOFT.NS", "CANBK.NS", "CGPOWER.NS", "CHOLAFIN.NS", "CIPLA.NS", "COALINDIA.NS", "COFORGE.NS", "COLPAL.NS", "CONCOR.NS", "COROMANDEL.NS", 
    "CROMPTON.NS", "CUMMINSIND.NS", "CYIENT.NS", "DABUR.NS", "DALBHARAT.NS", "DEEPAKNTR.NS", "DELHIVERY.NS", "DIVISLAB.NS", "DIXON.NS", "DLF.NS", 
    "DMART.NS", "DRREDDY.NS", "EICHERMOT.NS", "ESCORTS.NS", "EXIDEIND.NS", "FEDERALBNK.NS", "FORTIS.NS", "GAIL.NS", "GLAND.NS", "GLENMARK.NS", 
    "GMRINFRA.NS", "GODREJCP.NS", "GODREJPROP.NS", "GRASIM.NS", "GUJGASLTD.NS", "HAL.NS", "HAVELLS.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS", 
    "HEROMOTOCO.NS", "HINDALCO.NS", "HINDPETRO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "ICICIGI.NS", "ICICIPRULI.NS", "IDFCFIRSTB.NS", "IEX.NS", "IGL.NS", 
    "INDHOTEL.NS", "INDIACEM.NS", "INDIAMART.NS", "INDIGO.NS", "INDUSINDBK.NS", "INDUSTOWER.NS", "INFY.NS", "IOC.NS", "IPCALAB.NS", "IRCTC.NS", 
    "IRFC.NS", "ITC.NS", "JINDALSTEL.NS", "JSWENERGY.NS", "JSWSTEEL.NS", "JUBLFOOD.NS", "KOTAKBANK.NS", "KPITTECH.NS", "L&TFH.NS", "LTIM.NS", 
    "LT.NS", "LICI.NS", "LUPIN.NS", "M&M.NS", "M&MFIN.NS", "MANAPPURAM.NS", "MARICO.NS", "MARUTI.NS", "MAXHEALTH.NS", "MAZDOCK.NS", 
    "METROPOLIS.NS", "MFSL.NS", "MGL.NS", "MOTHERSON.NS", "MPHASIS.NS", "MRF.NS", "MUTHOOTFIN.NS", "NATIONALUM.NS", "NAVINFLUOR.NS", "NESTLEIND.NS", 
    "NMDC.NS", "NTPC.NS", "OBEROIRLTY.NS", "ONGC.NS", "PAGEIND.NS", "PATANJALI.NS", "PEL.NS", "PERSISTENT.NS", "PETRONET.NS", "PFC.NS", 
    "PHOENIXLTD.NS", "PIDILITIND.NS", "PIIND.NS", "PNB.NS", "POLYCAB.NS", "POONAWALLA.NS", "POWERGRID.NS", "PRESTIGE.NS", "RECLTD.NS", "RELIANCE.NS", 
    "SAIL.NS", "SBICARD.NS", "SBILIFE.NS", "SBIN.NS", "SHREECEM.NS", "SHRIRAMFIN.NS", "SIEMENS.NS", "SRF.NS", "SUNPHARMA.NS", "SUNTV.NS", 
    "SYNGENE.NS", "TATACOMM.NS", "TATACONSUM.NS", "TATAELXSI.NS", "TATAMOTORS.NS", "TATAPOWER.NS", "TATASTEEL.NS", "TCS.NS", "TECHM.NS", "TITAN.NS", 
    "TORNTPHARM.NS", "TRENT.NS", "TVSMOTOR.NS", "UBL.NS", "ULTRACEMCO.NS", "UNIONBANK.NS", "UNITDSPR.NS", "UPL.NS", "VBL.NS", "VEDL.NS", 
    "VOLTAS.NS", "WHIRLPOOL.NS", "WIPRO.NS", "YESBANK.NS", "ZEEL.NS", "ZOMATO.NS", "ZYDUSLIFE.NS"
]

# --------------------------------------------------
# FAST BATCH FETCH FUNCTION
# --------------------------------------------------
@st.cache_data(ttl=60) # Refresh every 1 minute
def fetch_nifty_data(symbols):
    # Batch download is much faster than individual tickers
    data = yf.download(symbols, period="1d", interval="1m", group_by='ticker', threads=True)
    
    rows = []
    for sym in symbols:
        try:
            # Getting latest price and previous close
            current_price = data[sym]['Close'].iloc[-1]
            prev_close = data[sym]['Open'].iloc[0] # Approx for live change
            
            change = current_price - prev_close
            pct_change = (change / prev_close) * 100
            
            rows.append({
                "Symbol": sym.replace(".NS", ""),
                "Price": round(current_price, 2),
                "Change": round(change, 2),
                "Percent Change": round(pct_change, 2)
            })
        except:
            continue
            
    return pd.DataFrame(rows)

# --------------------------------------------------
# APP LOGIC
# --------------------------------------------------
if st.button('🔄 Refresh Data'):
    st.cache_data.clear()

with st.spinner("Fetching Nifty 200 Live Data..."):
    df = fetch_nifty_data(nifty_200_symbols)

# Sidebar Filters
st.sidebar.header("🔍 Filters")
search = st.sidebar.text_input("Search Stock Symbol")
gainer = st.sidebar.checkbox("Show Gainers Only")
loser = st.sidebar.checkbox("Show Losers Only")

# Apply Filters
if search:
    df = df[df["Symbol"].str.contains(search.upper())]
if gainer:
    df = df[df["Percent Change"] > 0]
if loser:
    df = df[df["Percent Change"] < 0]

# Sorting
df = df.sort_values(by="Percent Change", ascending=False)

# Formatting and Display
st.success(f"✅ Showing {len(df)} Stocks")

# Custom Column Styling
def color_change(val):
    color = 'green' if val > 0 else 'red'
    return f'color: {color}'

st.dataframe(
    df.style.applymap(color_change, subset=['Change', 'Percent Change']),
    use_container_width=True,
    height=600
)
