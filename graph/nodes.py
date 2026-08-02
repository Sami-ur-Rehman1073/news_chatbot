from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from graph.state import GraphState
from utils.llm import llm
from prompts.system_prompt import TOPIC_EXTRACTION_PROMPT, SEARCH_PROMPT_TEMPLATE, ARTICLE_SUMMARIZATION_PROMPT
from search.duckduckgo_search import search_duckduckgo
from search.newsapi_search import search_newsapi
from search.gnews_search import search_gnews


def add_user_message(state):
    return {
        "chat_history": [
            HumanMessage(content=state["user_query"])
        ]
    }



def add_assistant_message(response):
    return {
        "assistant_response": response.content,
        "chat_history": [
            AIMessage(content=response.content)
        ]
    }


def user_input_node(state: GraphState) -> GraphState:
    """
    Stores the user's input in the graph state.
    """

    print("\n===== User Input Node =====")
    print(f"User Query: {state['user_query']}")

    return {
        "user_query": state["user_query"]
    }


def chatbot_node(state: GraphState):
    """
    Handles the chatbot conversation.
    """

    print("\n===== Chatbot Node =====")

    # Add current user message
    updated_history = state["chat_history"] + [
        HumanMessage(content=state["user_query"])
    ]

    # Invoke the LLM
    response = llm.invoke(updated_history)

    print(f"Assistant: {response.content}")

    return {
        "chat_history": [
            HumanMessage(content=state["user_query"]),
            AIMessage(content=response.content),
        ],
        "assistant_response": response.content,
    }




def topic_extraction_node(state: GraphState):

    print("\n===== Topic Extraction Node =====")

    messages = [
        SystemMessage(content=TOPIC_EXTRACTION_PROMPT),
        HumanMessage(content=state["user_query"])
    ]

    response = llm.invoke(messages)

    topic = response.content.strip()

    print(f"Extracted Topic: {topic}")

    return {
        "topic": topic
    }



def query_refinement_node(state: GraphState):
    """
    Builds the search prompt from the extracted topic.
    """

    print("\n===== Search Prompt Node =====")

    search_prompt = SEARCH_PROMPT_TEMPLATE.format(
        topic=state["topic"]
    )

    print(search_prompt)

    return {
        "search_query": search_prompt
    }





def duckduckgo_search_node(state: GraphState):
    """
    Search DuckDuckGo News.
    """

    print("\n===== DuckDuckGo Search Node =====")

    articles = search_duckduckgo(
        query=str(state["topic"])
    )

    print(f"Retrieved {len(articles)} articles.")

    return {
    "duckduckgo_articles": articles
    }


def newsapi_search_node(state: GraphState):

    print("\n===== NewsAPI Search Node =====")

    articles = search_newsapi(
    query=state["topic"]
    )

    print(f"Retrieved {len(articles)} articles.")

    return {
    "newsapi_articles": articles
    }





def gnews_search_node(state: GraphState):
    """
    Search GNews API.
    """

    print("\n===== GNews Search Node =====")

    articles = search_gnews(
        query=state["topic"]
    )

    print(f"Retrieved {len(articles)} articles.")

    return {
    "gnews_articles": articles
    }


def merge_results_node(state: GraphState):
    """
    Merge the results from all search engines into a single list.
    """

    print("\n===== Merge Results Node =====")

    merged_articles = []

    merged_articles.extend(state["duckduckgo_articles"])
    merged_articles.extend(state["newsapi_articles"])
    merged_articles.extend(state["gnews_articles"])

    print(f"DuckDuckGo Articles : {len(state['duckduckgo_articles'])}")
    print(f"NewsAPI Articles    : {len(state['newsapi_articles'])}")
    print(f"GNews Articles      : {len(state['gnews_articles'])}")
    print(f"Total Articles      : {len(merged_articles)}")

    return {
        "raw_articles": merged_articles
    }



def article_summarization_node(state: GraphState):

    print("\n===== Article Summarization Node =====")

    summarized_articles = []

    for article in state["raw_articles"]:

        prompt = f"""
{ARTICLE_SUMMARIZATION_PROMPT}

Article URL:
{article['url']}
"""

        response = llm.invoke(prompt)

        summarized_article = article.copy()

        summarized_article["content"] = response.content.strip()

        summarized_articles.append(summarized_article)

    print(f"Summarized {len(summarized_articles)} articles.")

    return {
        "summarized_articles": summarized_articles
    }