from graph.builder import build_graph

graph = build_graph()

state = {
    "user_query": "",
    "topic": "",
    "search_query": "",

    "duckduckgo_articles": [],
    "newsapi_articles": [],
    "gnews_articles": [],

    "raw_articles": [],
    "summarized_articles": [],
    "final_articles": [],

    "chat_history": [],
    "assistant_response": "",
}


while True:

    user_query = input("\nYou: ")

    if user_query.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    # Reset state for new query
    state["user_query"] = user_query
    state["topic"] = ""

    state["duckduckgo_articles"] = []
    state["newsapi_articles"] = []
    state["gnews_articles"] = []

    state["raw_articles"] = []
    state["summarized_articles"] = []
    state["final_articles"] = []

    state = graph.invoke(state)

    print("\n")
    print("=" * 100)
    print("SUMMARIZED ARTICLES")
    print("=" * 100)

    for index, article in enumerate(state["summarized_articles"], start=1):

        print(f"\nArticle {index}")
        print("-" * 100)
        print(f"Title          : {article['title']}")
        print(f"Source         : {article['source']}")
        print(f"Published      : {article['published_at']}")
        print(f"Search Engine  : {article['search_engine']}")
        print(f"URL            : {article['url']}")
        print("\nSummary:")
        print(article["content"])

    print("\n" + "=" * 100)