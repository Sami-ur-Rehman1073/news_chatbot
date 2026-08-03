# AI News Chatbot

An AI-powered News Chatbot that retrieves the latest news articles from multiple online news sources, summarizes each article using a Large Language Model (LLM), and presents concise, easy-to-read news updates through a FastAPI web application.

The chatbot follows a modular LangGraph workflow where every step of the news retrieval pipeline is represented as an independent node. Multiple search providers are queried in parallel, their results are normalized into a common format, merged together, and finally summarized before being displayed to the user.

---

# Features

* Search the latest news using natural language queries.
* Automatic topic extraction from user input.
* Parallel news retrieval from multiple sources.
* News aggregation from:

  * DuckDuckGo News
  * NewsAPI
  * GNews API
* Normalization of articles into a unified data structure.
* Merge results from multiple providers.
* AI-generated article summaries using Groq LLM.
* Clean and responsive web interface built with FastAPI and Tailwind CSS.
* Modular LangGraph workflow for easy extension.
* No database required.

---

# Project Workflow

```
User Query
      │
      ▼
User Input Node
      │
      ▼
Topic Extraction Node
      │
      ▼
Parallel Search Nodes
 ┌──────────────┬──────────────┬──────────────┐
 │              │              │
 ▼              ▼              ▼
DuckDuckGo   NewsAPI       GNews API
 │              │              │
 └──────────────┴──────────────┘
                │
                ▼
       Merge Results Node
                │
                ▼
   Article Summarization Node
                │
                ▼
         FastAPI Frontend
```

---

# Technologies Used

## Backend

* Python
* FastAPI
* LangGraph
* LangChain
* Groq API

## News Sources

* DuckDuckGo News
* NewsAPI
* GNews API

## Frontend

* HTML
* Tailwind CSS

## Environment Management

* python-dotenv

---

# Project Structure

```
news_chatbot/
│
├── app.py
├── main.py
├── requirements.txt
├── .env
│
├── graph/
│   ├── builder.py
│   ├── nodes.py
│   ├── prompts.py
│   └── state.py
│  
│
├── search/
│   ├── duckduckgo_search.py
│   ├── newsapi_search.py
│   └── gnews_search.py
│
├── templates/
│   └── index.html
│
└── utils/
    └── llm.py
```

---

# LangGraph Pipeline

## 1. User Input Node

Receives the user's query and stores it in the graph state.

---

## 2. Topic Extraction Node

Extracts the primary news topic from the user's natural language query.

Example:

**Input**

```
What is happening between Iran and the United States?
```

**Extracted Topic**

```
US-Iran conflict
```

---

## 3. Parallel Search Nodes

Three independent search nodes execute simultaneously.

* DuckDuckGo News
* NewsAPI
* GNews API

Each node retrieves recent news articles related to the extracted topic.

---

## 4. Article Normalization

Articles from all providers are converted into a common format.

```python
{
    "title": "",
    "description": "",
    "content": "",
    "url": "",
    "source": "",
    "published_at": ""
}
```

This ensures that downstream processing is independent of the news provider.

---

## 5. Merge Results Node

Collects normalized articles from all search providers into a single list.

---

## 6. Article Summarization Node

Each article URL is provided to the Groq Large Language Model.

The model:

* Reads the article
* Understands its content
* Generates a concise summary
* Stores the summary in the `content` field

The remaining article metadata remains unchanged.

---

## 7. Frontend

The summarized articles are rendered in a clean user interface displaying:

* Article title
* AI-generated summary
* News source
* Publication date
* Original article link

---

# Installation

Clone the repository

```bash
git clone <repository-url>
cd news_chatbot
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY

NEWSAPI_API_KEY=YOUR_NEWSAPI_KEY

GNEWS_API_KEY=YOUR_GNEWS_API_KEY
```

---

# Running the Project

Start the FastAPI application.

```bash
uvicorn app:app --reload
```

Open your browser.

```
http://127.0.0.1:8000
```

---

# Future Improvements

* Duplicate article detection using an LLM.
* Re-ranking articles based on relevance.
* Streaming responses.
* Source reliability scoring.
* Support for additional news providers.
* Multi-language news retrieval.
* Cached search results for improved performance.
* User authentication and personalized news preferences.


