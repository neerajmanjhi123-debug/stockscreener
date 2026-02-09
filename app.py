import streamlit as st
import pandas as pd
import yfinance as yf
from streamlit_autorefresh import st_autorefresh

# 1. Page Configuration
st.set_page_config(page_title="Nifty 200 Real-Time Dashboard", layout="wide")

# 2. Auto-Refresh Setup (Har 30 seconds mein page refresh hoga)
st_autorefresh(interval=30 * 1000, key="nifty200refresh")

st.title("📊 Nifty 200 Live Market Dashboard")
st.markdown(f"**Last Updated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 3. Data Fetching Function (Cached for performance)
@st.cache_data
def get_nifty200_list():
    url = "https://archives.nseindia.com/content/indices/ind_nifty200list.csv"
    try:
        df = pd.read_csv(url)
        # yfinance ke liye ticker prepare karna (.NS suffix)
        df['Ticker'] = df['Symbol'] + ".NS"
        return df
    except Exception as e:
        st.error(f"Error fetching list: {e}")
        return None

# 4. Live Price Fetching Function
def fetch_live_prices(tickers):
    # Ek saath saare tickers ka data fetch karna faster hota hai
    data = yf.download(tickers, period="1d", interval="1m", group_by='ticker', progress=False)
    
    price_dict = {}
    for ticker in tickers:
        try:
            # Latest closing price nikalna
            current_price = data[ticker]['Close'].iloc[-1]
            price_dict[ticker] = round(current_price, 2)
        except:
            price_dict[ticker] = "N/A"
    return price_dict

# --- Main Logic ---

df_stocks = get_nifty200_list()

if df_stocks is not None:
    with st.spinner('Fetching Live Prices...'):
        # Sirf tickers ki list nikal kar prices fetch karna
        tickers_list = df_stocks['Ticker'].tolist()
        live_prices = fetch_live_prices(tickers_list)
        
        # DataFrame mein prices add karna
        df_stocks['Live Price (₹)'] = df_stocks['Ticker'].map(live_prices)

    # 5. UI Layout - Filters
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_sector = st.multiselect("Sector Filter:", options=df_stocks['Industry'].unique())
    
    # Filter Logic
    if selected_sector:
        df_display = df_stocks[df_stocks['Industry'].isin(selected_sector)]
    else:
        df_display = df_stocks

    # 6. Display Data Table
    # Re-arranging columns for better view
    display_cols = ['Symbol', 'Company Name', 'Industry', 'Live Price (₹)']
    
    st.dataframe(
        df_display[display_cols].reset_index(drop=True), 
        use_container_width=True,
        height=600
    )

    # 7. Summary Stats
    st.sidebar.header("Market Summary")
    st.sidebar.metric("Total Stocks", len(df_stocks))
    st.sidebar.info("Dashboard 30 seconds mein auto-refresh ho raha hai.")
    
    # Download Link
    csv = df_display.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button("Download CSV", csv, "nifty200_live.csv", "text/csv")

else:
    st.error("NSE se list load nahi ho saki.")
