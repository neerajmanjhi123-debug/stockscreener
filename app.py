import pandas as pd
import requests

def get_nifty_200_stocks():
    # NSE official link for Nifty 200 index constituents
    url = "https://archives.nseindia.com/content/indices/ind_nifty200list.csv"
    
    # Adding headers to mimic a browser request (important for NSE)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # CSV data ko pandas dataframe mein load karna
            with open("nifty200.csv", "wb") as f:
                f.write(response.content)
            
            df = pd.read_csv("nifty200.csv")
            
            # Sirf Stock Symbol aur Company Name dikhana
            print(f"Total Stocks Found: {len(df)}")
            print("-" * 30)
            print(df[['Symbol', 'Company Name']])
            
            return df
        else:
            print("Failed to fetch data from NSE.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_nifty_200_stocks()
