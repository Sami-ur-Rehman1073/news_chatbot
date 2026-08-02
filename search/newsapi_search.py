import os
import requests

from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWSAPI_API_KEY")


def search_newsapi(query: str, page_size: int = 5):
    """
    Search NewsAPI and return normalized articles.
    """

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": query,
        "pageSize": page_size,
        "sortBy": "publishedAt",
        "language": "en",
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(url, params=params)
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
        "search_engine": "NewsAPI"
    }

        articles.append(normalized_article)

    return articles