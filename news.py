import requests

API_KEY = "693bc4554a9a4bb480fea97eb0268104"

def get_news(country, category):
    # 🎯 Primary endpoint (country + category)
    url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={API_KEY}"
    
    data = requests.get(url).json()

    # Debug (optional)
    # print(data)

    # ❗ Fallback if no results
    if "articles" not in data or len(data["articles"]) == 0:
        fallback_url = f"https://newsapi.org/v2/everything?q={category}&language=en&sortBy=publishedAt&apiKey={API_KEY}"
        data = requests.get(fallback_url).json()

        if "articles" not in data:
            return []

    # ✅ Extract full article details
    articles = []
    for article in data["articles"][:5]:
        articles.append({
            "title": article.get("title", "No title available"),
            "url": article.get("url", "#"),
            "image": article.get("urlToImage")
        })

    return articles