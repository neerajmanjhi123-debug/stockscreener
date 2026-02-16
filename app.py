import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Nifty 200 Live Screener", layout="wide")
st.title("📊 Nifty 200 Live Screener")

# --------------------------------------------------
# COMPLETE NIFTY 200 LIST (Updated)
# --------------------------------------------------
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

# --------------------------------------------------
# LIVE FETCHING
# --------------------------------------------------
@st.cache_data(ttl=60)
def fetch_live_data(tickers):
    # Fetching 2 days of data to compare Today's Open with Yesterday's Close (for Gap Up/Down)
    data = yf.download(tickers, period="2d", interval="1d", group_by='ticker', progress=False)
    
    rows = []
    for ticker in tickers:
        try:
            stock_data = data[ticker]
            current_price = stock_data['Close'].iloc[-1]
            prev_close = stock_data['Close'].iloc[-2]
            today_open = stock_data['Open'].iloc[-1]
            
            change = current_price - prev_close
            pct_change = (change / prev_close) * 100
            
            # Gap Calculation
            gap_pct = ((today_open - prev_close) / prev_close) * 100

            rows.append({
                "Symbol": ticker.replace(".NS", ""),
                "Price": current_price,
                "Change": change,
                "Percent Change": pct_change,
                "Gap %": gap_pct
            })
        except:
            continue
    return pd.DataFrame(rows)

# Load Data
with st.spinner("Fetching Nifty 200 Live Data..."):
    df = fetch_live_data(nifty_200_tickers)

# --------------------------------------------------
# FILTERS
# --------------------------------------------------
st.sidebar.header("🔍 Stock Filters")
filter_type = st.sidebar.radio(
    "Select View:",
    ["All Stocks", "Gainer", "Loser", "Gap Up", "Gap Down"]
)

# Apply Logic
filtered_df = df.copy()

if filter_type == "Gainer":
    filtered_df = filtered_df[filtered_df["Percent Change"] > 0]
elif filter_type == "Loser":
    filtered_df = filtered_df[filtered_df["Percent Change"] < 0]
elif filter_type == "Gap Up":
    filtered_df = filtered_df[filtered_df["Gap %"] > 0.5] # Min 0.5% Gap
elif filter_type == "Gap Down":
    filtered_df = filtered_df[filtered_df["Gap %"] < -0.5]

# Sorting
filtered_df = filtered_df.sort_values(by="Percent Change", ascending=False)

# --------------------------------------------------
# FORMATTING & DISPLAY
# --------------------------------------------------
st.subheader(f"📋 {filter_type} List ({len(filtered_df)})")

# Decimal formatting to .00
formatted_df = filtered_df.copy()
formatted_df["Price"] = formatted_df["Price"].map("{:.2f}".format)
formatted_df["Change"] = formatted_df["Change"].map("{:.2f}".format)
formatted_df["Percent Change"] = formatted_df["Percent Change"].map("{:.2f}%".format)
formatted_df["Gap %"] = formatted_df["Gap %"].map("{:.2f}%".format)

# Display table
st.dataframe(
    formatted_df[["Symbol", "Price", "Change", "Percent Change", "Gap %"]],
    use_container_width=True,
    hide_index=True
)

st.success("✅ Live Data Updated")
