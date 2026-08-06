from langgraph.graph import StateGraph, END

from graph.state import GraphState
from graph.nodes import overall_summary_node


def build_summary_graph():

    graph = StateGraph(GraphState)

    graph.add_node(
        "overall_summary",
        overall_summary_node
    )

    graph.set_entry_point("overall_summary")

    graph.add_edge(
        "overall_summary",
        END
    )

    return graph.compile()