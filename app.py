import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Nifty 200 Stock List", layout="wide")

st.title("📊 Nifty 200 Stocks List")
st.markdown("Yeh app NSE ki official website se Nifty 200 stocks ki live list fetch karti hai.")

@st.cache_data # Data ko baar-baar download hone se rokne ke liye
def load_data():
    url = "https://archives.nseindia.com/content/indices/ind_nifty200list.csv"
    try:
        # NSE data fetch karne ke liye pandas ka use
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Data load karne mein error aaya: {e}")
        return None

# Data Load Karein
data = load_data()

if data is not None:
    # Sidebar Filters
    st.sidebar.header("Filter Options")
    search = st.sidebar.text_input("Stock Symbol Search:")

    if search:
        data = data[data['Symbol'].str.contains(search.upper())]

    # Metrics
    col1, col2 = st.columns(2)
    col1.metric("Total Stocks", len(data))
    col2.metric("Index", "Nifty 200")

    # Display Table
    st.dataframe(data, use_container_width=True)

    # Download Button
    csv = data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download List as CSV",
        data=csv,
        file_name='nifty200_list.csv',
        mime='text/csv',
    )
else:
    st.write("Filhaal data available nahi hai.")
