from ddgs import DDGS


def search_duckduckgo(query: str, max_results: int = 5):
    """
    Search DuckDuckGo News and return normalized articles.
    """

    articles = []

    with DDGS() as ddgs:

        results = ddgs.news(
            query=query,
            max_results=max_results
        )

        for article in results:

            normalized_article = {
                "title": article.get("title", ""),
                "description": article.get("body", ""),
                "content": "",
                "url": article.get("url", ""),
                "source": article.get("source", ""),
                "published_at": article.get("date", ""),
                "search_engine": "DuckDuckGo"
            }

            articles.append(normalized_article)

    return articles