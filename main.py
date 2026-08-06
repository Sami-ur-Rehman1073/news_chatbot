from graph.builder import build_graph
from graph.summary_builder import build_summary_graph


# Build graphs once
graph = build_graph()
summary_graph = build_summary_graph()


state = {
    "user_query": "",
    "topic": "",
    "search_query": "",

    # Search engine results
    "duckduckgo_articles": [],
    "newsapi_articles": [],
    "gnews_articles": [],

    # Merged articles
    "raw_articles": [],

    # Summarized articles
    "summarized_articles": [],

    # Duplicate indexes returned by the LLM
    "duplicate_indexes": [],

    # Final articles after duplicate removal
    "final_articles": [],

    # Chat history
    "chat_history": [],

    # Latest assistant response
    "assistant_response": ""
}


while True:

    user_query = input("\nYou: ")

    if user_query.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    # Reset state
    state["user_query"] = user_query
    state["topic"] = ""
    state["search_query"] = ""

    state["duckduckgo_articles"] = []
    state["newsapi_articles"] = []
    state["gnews_articles"] = []

    state["raw_articles"] = []
    state["summarized_articles"] = []

    state["duplicate_indexes"] = []
    state["final_articles"] = []

    # Execute LangGraph
    state = graph.invoke(state)

    print("\n")
    print("=" * 100)
    print("FINAL UNIQUE ARTICLES")
    print("=" * 100)

    print(f"\nTotal Articles After Duplicate Removal: {len(state['final_articles'])}")

    for index, article in enumerate(state["final_articles"], start=1):

        print("\n" + "-" * 100)
        print(f"Article {index}")
        print("-" * 100)

        print(f"Title         : {article['title']}")
        print(f"Source        : {article['source']}")
        print(f"Published     : {article['published_at']}")

        if "search_engine" in article:
            print(f"Search Engine : {article['search_engine']}")

        print(f"URL           : {article['url']}")

        print("\nSummary:")
        print(article["content"])

    print("\n" + "=" * 100)