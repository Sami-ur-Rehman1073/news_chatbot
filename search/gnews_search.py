import os
import requests

from dotenv import load_dotenv

load_dotenv()

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")


def search_gnews(query: str, max_results: int = 5):

    url = "https://gnews.io/api/v4/search"

    params = {
        "q": query,
        "lang": "en",
        "max": max_results,
        "apikey": GNEWS_API_KEY
    }

    response = requests.get(url, params=params)

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    response.raise_for_status()

    data = response.json()

    articles = []

    for article in data.get("articles", []):

        normalized_article = {
        "title": article.get("title", ""),
        "description": article.get("description", ""),
        "content": article.get("content", ""),
        "url": article.get("url", ""),
        "source": article.get("source", {}).get("name", ""),
        "published_at": article.get("publishedAt", ""),
        "search_engine": "GNews"
    }

        articles.append(normalized_article)

    return articles