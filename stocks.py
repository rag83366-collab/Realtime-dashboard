import requests
import time

API_KEY = "8U4M09CT7SD4GQLH"

# 📈 Stock time series data (for graph)
def get_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    
    time.sleep(1)  # ⏳ prevent rate limit
    
    data = requests.get(url).json()

    # Debug (optional)
    # print(data)

    if "Time Series (Daily)" not in data:
        return None

    return data["Time Series (Daily)"]


# 🏢 Company info (name + industry + metrics)
def get_company_info(symbol):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}"
    
    time.sleep(1)  # ⏳ prevent rate limit
    
    data = requests.get(url).json()

    # Debug (optional)
    # print(data)

    if "Name" not in data:
        return {
            "name": symbol,
            "industry": "N/A",
            "market_cap": "N/A",
            "pe_ratio": "N/A"
        }

    return {
        "name": data.get("Name", symbol),
        "industry": data.get("Industry", "N/A"),
        "market_cap": data.get("MarketCapitalization", "N/A"),
        "pe_ratio": data.get("PERatio", "N/A")
    }