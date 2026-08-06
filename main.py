from graph.builder import build_graph
from graph.summary_builder import build_summary_graph


# Build graphs once
graph = build_graph()
summary_graph = build_summary_graph()


# Initial graph state
state = {
    "user_query": "",
    "topic": "",
    "search_query": "",

    "duckduckgo_articles": [],
    "newsapi_articles": [],
    "gnews_articles": [],

    "raw_articles": [],
    "summarized_articles": [],
    "overall_summary": "",
    "final_articles": [],

    "chat_history": [],
    "assistant_response": "",
}


while True:

    user_query = input("\nYou: ")

    if user_query.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    # Reset state for a new search
    state["user_query"] = user_query
    state["topic"] = ""
    state["search_query"] = ""

    state["duckduckgo_articles"] = []
    state["newsapi_articles"] = []
    state["gnews_articles"] = []

    state["raw_articles"] = []
    state["summarized_articles"] = []
    state["overall_summary"] = ""
    state["final_articles"] = []

    # Run search workflow
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

    # Ask whether to generate an overall summary
    choice = input("\nGenerate overall summary? (y/n): ")

    if choice.lower() == "y":

        summary_state = {
            "user_query": "",
            "topic": "",
            "search_query": "",

            "duckduckgo_articles": [],
            "newsapi_articles": [],
            "gnews_articles": [],

            "raw_articles": [],
            "summarized_articles": state["summarized_articles"],
            "overall_summary": "",
            "final_articles": [],

            "chat_history": [],
            "assistant_response": ""
        }

        summary_state = summary_graph.invoke(summary_state)

        print("\n")
        print("=" * 100)
        print("OVERALL NEWS SUMMARY")
        print("=" * 100)
        print(summary_state["overall_summary"])
        print("=" * 100)