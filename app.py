from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from graph.builder import build_graph


app = FastAPI(title="AI News Chatbot")

# Mount static directory (for future CSS/images if needed)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Build LangGraph once at startup
graph = build_graph()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Display empty search page.
    """

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "query": "",
            "articles": []
        }
    )


@app.post("/search", response_class=HTMLResponse)
async def search_news(
    request: Request,
    query: str = Form(...)
):
    """
    Execute the LangGraph workflow and display results.
    """

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

        articles = result.get("summarized_articles", [])

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "query": query,
                "articles": articles
            }
        )

    except Exception as e:

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "query": query,
                "articles": [],
                "error": str(e)
            }
        )