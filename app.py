import streamlit as st
from weather import get_weather
from stocks import get_stock_data, get_company_info
from news import get_news
import plotly.graph_objects as go

# 🎨 Page config
st.set_page_config(
    page_title="Real-Time Data Dashboard",
    page_icon="📊",
    layout="wide"
)

# 🎨 Premium CSS
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #eef2f3, #dfe9f3);
    color: #1a1a1a;
}

.stMetric {
    background: rgba(255,255,255,0.8) !important;
    backdrop-filter: blur(10px);
    padding: 18px;
    border-radius: 15px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    text-align: center;
}

.news-card {
    background: white;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# 🎯 Header
st.markdown("## 🌍 Real-Time Data Dashboard")
st.caption("Live Weather • Stock Market • News Analytics")

# 🎛️ Sidebar
st.sidebar.title("⚙️ Settings")

# 🌍 City dropdown
cities = ["Bangalore", "Mumbai", "Delhi", "Hyderabad", "Chennai", "New York", "London"]
city = st.sidebar.selectbox("Select City", cities)

# 📈 Company dropdown
companies = {
    "Apple": "AAPL",
    "Tesla": "TSLA",
    "Google": "GOOGL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Meta": "META"
}
company_name = st.sidebar.selectbox("Select Company", list(companies.keys()))
symbol = companies[company_name]

# 🌐 Country dropdown
countries = {
    "India 🇮🇳": "in",
    "USA 🇺🇸": "us",
    "UK 🇬🇧": "gb",
    "Canada 🇨🇦": "ca",
    "Australia 🇦🇺": "au"
}
country_name = st.sidebar.selectbox("Select News Country", list(countries.keys()))
country = countries[country_name]

# 🏷️ Category dropdown
categories = {
    "Technology 💻": "technology",
    "Business 💼": "business",
    "Sports ⚽": "sports",
    "Health 🏥": "health",
    "Science 🔬": "science",
    "Entertainment 🎬": "entertainment"
}
category_name = st.sidebar.selectbox("Select News Category", list(categories.keys()))
category = categories[category_name]

# ✅ CACHE
@st.cache_data(ttl=120)
def load_stock(symbol):
    return get_stock_data(symbol), get_company_info(symbol)

@st.cache_data(ttl=120)
def load_news(country, category):
    return get_news(country, category)

# 🧱 Layout
col1, col2 = st.columns(2)

# 🌦️ WEATHER
with col1:
    st.markdown("### 🌦️ Weather")

    with st.spinner("Fetching weather..."):
        weather = get_weather(city)

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #74ebd5, #9face6);
        padding: 25px;
        border-radius: 18px;
        text-align: center;
    ">
        <h2>{city}</h2>
        <h1>{weather['temp']}°C</h1>
        <p>{weather['condition']}</p>
        <p>💧 Humidity: {weather['humidity']}%</p>
    </div>
    """, unsafe_allow_html=True)

# 📈 STOCK
    st.markdown("### 📈 Stock Dashboard")

    with st.spinner("Fetching stock data..."):
        data, info = load_stock(symbol)

    st.markdown(f"""
        <div style="text-align:center;">
            <h2>{info['name']}</h2>
            <p style="color:gray;">{info['industry']}</p>
        </div>
    """, unsafe_allow_html=True)

    if data:
        dates = list(data.keys())[:10]
        prices = [float(data[d]["4. close"]) for d in dates]

        latest_price = prices[0]
        prev_price = prices[1]
        change = latest_price - prev_price

        m1, m2, m3 = st.columns(3)

        trend = "📈" if change >= 0 else "📉"

        m1.metric("Price 💰", f"${latest_price:.2f}", f"{trend} {change:.2f}")
        m2.metric("Market Cap 📦", info['market_cap'])
        m3.metric("P/E Ratio 📊", info['pe_ratio'])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates[::-1],
            y=prices[::-1],
            mode='lines+markers',
            name=symbol
        ))

        fig.update_layout(
            title="📊 Stock Price Trend",
            template="plotly_white",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("⏳ API limit reached. Please wait a minute and try again.")

# 📰 NEWS
st.markdown("### 📰 Latest News")

with st.spinner("Fetching news..."):
    news = load_news(country, category)

for article in news:
    st.markdown(f"""
    <div class="news-card">
        <h4>{article['title']}</h4>
        <a href="{article['url']}" target="_blank">Read more</a>
    </div>
    """, unsafe_allow_html=True)

    if article["image"]:
        st.image(article["image"])