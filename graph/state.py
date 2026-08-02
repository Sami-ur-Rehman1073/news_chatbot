from typing import Annotated

from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class GraphState(TypedDict):
    # Current user query
    user_query: str

    # Extracted topic
    topic: str

    # Search query
    search_query: str

    # Individual search engine results
    duckduckgo_articles: list[dict]
    newsapi_articles: list[dict]
    gnews_articles: list[dict]

    # Merged articles
    raw_articles: list[dict]

    # Articles after summarization
    summarized_articles: list[dict]

    # Final articles after duplicate removal
    final_articles: list[dict]

    # Conversation history
    chat_history: Annotated[list[BaseMessage], add_messages]

    # Latest assistant response
    assistant_response: str