from langgraph.graph import StateGraph, START, END

from graph.state import GraphState
from graph.nodes import (
    user_input_node,
    topic_extraction_node,
    query_refinement_node,
    duckduckgo_search_node,
    newsapi_search_node,
    gnews_search_node,
    merge_results_node,
    article_summarization_node,
    duplicate_detection_node,
    duplicate_filter_node,
)


def build_graph():

    workflow = StateGraph(GraphState)

    # Nodes
    workflow.add_node("user_input", user_input_node)
    workflow.add_node("topic_extraction", topic_extraction_node)
    workflow.add_node("query_refinement", query_refinement_node)

    workflow.add_node("duckduckgo_search", duckduckgo_search_node)
    workflow.add_node("newsapi_search", newsapi_search_node)
    workflow.add_node("gnews_search", gnews_search_node)

    workflow.add_node("merge_results", merge_results_node)

    workflow.add_node(
        "article_summarization",
        article_summarization_node
    )

    workflow.add_node(
        "duplicate_detection",
        duplicate_detection_node
    )

    workflow.add_node(
        "duplicate_filter",
        duplicate_filter_node
    )

    # Initial flow
    workflow.add_edge(START, "user_input")
    workflow.add_edge("user_input", "topic_extraction")
    workflow.add_edge("topic_extraction", "query_refinement")

    # Parallel search
    workflow.add_edge(
        "query_refinement",
        "duckduckgo_search"
    )

    workflow.add_edge(
        "query_refinement",
        "newsapi_search"
    )

    workflow.add_edge(
        "query_refinement",
        "gnews_search"
    )

    # Merge after all searches complete
    workflow.add_edge(
        "duckduckgo_search",
        "merge_results"
    )

    workflow.add_edge(
        "newsapi_search",
        "merge_results"
    )

    workflow.add_edge(
        "gnews_search",
        "merge_results"
    )

    # Remaining pipeline
    workflow.add_edge(
        "merge_results",
        "article_summarization"
    )

    workflow.add_edge(
        "article_summarization",
        "duplicate_detection"
    )

    workflow.add_edge(
        "duplicate_detection",
        "duplicate_filter"
    )

    workflow.add_edge(
        "duplicate_filter",
        END
    )

    return workflow.compile()