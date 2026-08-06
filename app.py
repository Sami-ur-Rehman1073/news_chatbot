from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from graph.builder import build_graph
from utils.llm import llm
from prompts.system_prompt import NEWS_SUMMARIZATION_PROMPT


app = FastAPI(title="AI News Chatbot")

templates = Jinja2Templates(directory="templates")

graph = build_graph()

# Store latest search result (for demo)
latest_articles = []


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "query": "",
            "articles": [],
            "overall_summary": ""
        }
    )


@app.post("/search", response_class=HTMLResponse)
async def search_news(
    request: Request,
    query: str = Form(...)
):

    global latest_articles

    state = {
        "user_query": query,
        "topic": "",
        "search_query": "",

        "duckduckgo_articles": [],
        "newsapi_articles": [],
        "gnews_articles": [],

        "raw_articles": [],
        "summarized_articles": [],
        "final_articles": [],

        "chat_history": [],
        "assistant_response": ""
    }

    try:

        result = graph.invoke(state)

        latest_articles = result.get("summarized_articles", [])

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "query": query,
                "articles": latest_articles,
                "overall_summary": ""
            }
        )

    except Exception as e:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "query": query,
                "articles": [],
                "overall_summary": "",
                "error": str(e)
            }
        )


@app.post("/summarize-news", response_class=HTMLResponse)
async def summarize_news(request: Request):

    global latest_articles

    if not latest_articles:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "query": "",
                "articles": [],
                "overall_summary": "No articles available. Please search first."
            }
        )

    articles_text = ""

    for i, article in enumerate(latest_articles, start=1):

        articles_text += f"""
Article {i}

Title: {article['title']}

Summary:
{article['content']}

"""

    prompt = f"""
{NEWS_SUMMARIZATION_PROMPT}

News Articles:

{articles_text}
"""

    response = llm.invoke(prompt)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "query": "",
            "articles": latest_articles,
            "overall_summary": response.content
        }
    )