from langgraph.graph import START, END, StateGraph

from graph.state import GraphState

from graph.nodes import (
    user_input_node,
    topic_extraction_node,
    duckduckgo_search_node,
    newsapi_search_node,
    gnews_search_node,
    merge_results_node,
    article_summarization_node
)


def build_graph():

    builder = StateGraph(GraphState)

    # Nodes
    builder.add_node("user_input", user_input_node)
    builder.add_node("topic_extraction", topic_extraction_node)

    builder.add_node("duckduckgo_search", duckduckgo_search_node)
    builder.add_node("newsapi_search", newsapi_search_node)
    builder.add_node("gnews_search", gnews_search_node)

    builder.add_node("merge_results", merge_results_node)
    builder.add_node("article_summarization", article_summarization_node)

    # Workflow
    builder.add_edge(START, "user_input")
    builder.add_edge("user_input", "topic_extraction")

    # Parallel search
    builder.add_edge("topic_extraction", "duckduckgo_search")
    builder.add_edge("topic_extraction", "newsapi_search")
    builder.add_edge("topic_extraction", "gnews_search")

    # Merge
    builder.add_edge("duckduckgo_search", "merge_results")
    builder.add_edge("newsapi_search", "merge_results")
    builder.add_edge("gnews_search", "merge_results")

    # Summarization
    builder.add_edge("merge_results", "article_summarization")

    builder.add_edge("article_summarization", END)

    return builder.compile()