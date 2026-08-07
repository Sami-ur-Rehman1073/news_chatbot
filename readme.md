# AI News Chatbot

An AI-powered News Chatbot that retrieves the latest news articles from multiple online news sources, summarizes each article using a Large Language Model (LLM), removes duplicate articles, verifies publisher credibility, generates an overall summary of the latest news, and presents the results through a FastAPI web application.

The chatbot follows a modular **LangGraph** workflow where each stage of the news retrieval pipeline is implemented as an independent node. Multiple search providers are queried in parallel, their results are normalized into a common structure, merged together, summarized, deduplicated, verified for source credibility, and finally displayed in a clean Tailwind CSS interface.

---

# Features

- Search the latest news using natural language queries.
- Automatic topic extraction using an LLM.
- Parallel news retrieval from multiple news providers.
- News aggregation from:
  - DuckDuckGo News
  - NewsAPI
  - GNews API
- Normalization of articles into a unified data structure.
- Merge results from multiple providers.
- AI-generated summaries for every news article using Groq LLM.
- AI-generated overall summary of all retrieved news articles.
- LLM-based duplicate article detection.
- Python-based duplicate filtering while retaining the latest article.
- Source credibility verification using trusted news organizations.
- Clean and responsive web interface built with FastAPI and Tailwind CSS.
- Modular LangGraph workflow for easy extension.
- No database required.

---

# Project Workflow

```text
                      User Query
                           │
                           ▼
                    User Input Node
                           │
                           ▼
                 Topic Extraction Node
                           │
                           ▼
               ┌─────────────────────────┐
               │ Parallel Search Nodes   │
               └─────────────────────────┘
                │         │          │
                ▼         ▼          ▼
         DuckDuckGo   NewsAPI    GNews API
                │         │          │
                └─────────┴──────────┘
                          │
                          ▼
                 Merge Results Node
                          │
                          ▼
            Article Summarization Node
                          │
                          ▼
          Duplicate Detection Node (LLM)
                          │
                          ▼
        Duplicate Filtering Node (Python)
                          │
                          ▼
       Source Credibility Verification
                          │
                          ▼
        Overall News Summarization Node
                          │
                          ▼
               FastAPI + Tailwind CSS
```

---

# Technologies Used

## Backend

- Python
- FastAPI
- LangGraph
- LangChain
- Groq API

## News Sources

- DuckDuckGo News
- NewsAPI
- GNews API

## Frontend

- HTML
- Tailwind CSS

## AI Features

- Topic Extraction
- Article Summarization
- Overall News Summarization
- Duplicate Detection
- Source Credibility Verification

## Environment Management

- python-dotenv

---

# Project Structure

```text
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
│   ├── state.py
│
├── prompts/
│   └── system_prompt.py
│
├── search/
│   ├── duckduckgo_search.py
│   ├── newsapi_search.py
│   └── gnews_search.py
│
├── templates/
│   └── index.html
│
├── utils/
│   ├── llm.py
│   └── trusted_sources.py
│
└── static/
```

---

# LangGraph Pipeline

## 1. User Input Node

Receives the user's natural language query and stores it in the graph state.

---

## 2. Topic Extraction Node

Uses a Large Language Model to extract the primary news topic from the user's query.

### Example

**Input**

```text
What is happening between Iran and Israel?
```

**Extracted Topic**

```text
Iran-Israel conflict
```

---

## 3. Parallel Search Nodes

Three independent search nodes execute simultaneously.

- DuckDuckGo News
- NewsAPI
- GNews API

Each node retrieves the latest news articles related to the extracted topic.

Executing the searches in parallel significantly reduces the overall response time.

---

## 4. Article Normalization

Each news provider returns a different JSON structure.

Every search node converts its results into the following common format:

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

Using a common schema allows all downstream nodes to work independently of the news provider.

---

## 5. Merge Results Node

Collects the normalized articles returned from every search provider into a single list.

At this stage, duplicate articles from different providers may still exist.

---

## 6. Article Summarization Node

Each article URL is provided to the Groq Large Language Model.

The model:

- Reads the article
- Understands its content
- Generates a concise summary
- Stores the generated summary in the `content` field

The remaining article metadata remains unchanged.

---

## 7. Duplicate Detection Node (LLM)

The summarized articles are sent to the Large Language Model.

Instead of comparing only article titles or URLs, the model compares the semantic meaning of the articles to identify duplicates.

The model returns the indexes of duplicate articles while preserving the index of the newest article.

Example:

```text
Duplicate Indexes

[2, 7, 11]
```

---

## 8. Duplicate Filtering Node (Python)

A Python node receives the duplicate indexes returned by the LLM.

The node removes duplicate articles while keeping the latest version based on the publication date.

The resulting unique articles are stored in:

```python
state["final_articles"]
```

These articles are used for all subsequent processing and displayed to the user.

---

## 9. Source Credibility Verification

Each unique article is compared against a predefined list of trusted news organizations.

If the publisher matches a trusted organization, the article is labeled as:

- ✅ Trusted Source

Otherwise, it is labeled as:

- ⚠️ Unverified Source

This information is stored with every article and displayed on the frontend.

---

## 10. Overall News Summarization Node

Instead of summarizing individual articles, this node summarizes the complete collection of unique news articles.

The LLM receives:

- Article titles
- Individual summaries

It generates a concise overview highlighting the major developments across all retrieved news.

The summary is displayed when the user clicks the **Summarize News** button.

---

## 11. Frontend

The FastAPI application renders the final news articles in a clean Tailwind CSS interface.

Each article displays:

- Title
- AI-generated summary
- Source
- Publication date
- Source credibility label
- Original article link

Users can also click the **Summarize News** button to generate a concise AI-generated summary covering all retrieved articles.

---

# Source Credibility Verification

The chatbot includes a **Source Credibility Verification** feature that helps users quickly assess the reliability of news articles based on their publishing source.

## How It Works

1. News articles are retrieved from multiple search providers.
2. The articles are normalized into a common structure.
3. Duplicate articles are removed.
4. Each article's publisher is compared against a predefined list of trusted news organizations.
5. If the publisher matches a trusted organization, the article is labeled as **Trusted Source**.
6. Otherwise, the article is labeled as **Unverified Source**.

The verification is performed using a keyword-based matching approach.

Examples of trusted publishers include:

- Reuters
- BBC
- Associated Press
- CNN
- Bloomberg
- The New York Times
- The Washington Post
- Al Jazeera
- The Guardian
- CNBC

## User Interface

Each article displays one of the following labels:

- ✅ Trusted Source
- ⚠️ Unverified Source

This enables users to quickly identify whether an article originates from a well-known news organization.

## Disclaimer

This feature **does not perform fake news detection or fact-checking**.

It only verifies whether the publisher belongs to a predefined list of trusted news organizations.

Articles labeled as **Unverified Source** are **not necessarily false or misleading**; they simply originate from publishers that are not currently included in the trusted source list.

Users are encouraged to verify important information through multiple reputable news sources.

---

# Installation

Clone the repository.

```bash
git clone <repository-url>
cd news_chatbot
```

Create a virtual environment.

```bash
python -m venv venv
```

Activate the environment.

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install the required packages.

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

Start the FastAPI server.

```bash
uvicorn app:app --reload
```

Open your browser.

```text
http://127.0.0.1:8000
```

---

# Future Improvements

- Advanced fake news detection using AI-based fact verification.
- Source reputation scoring based on historical credibility.
- Re-ranking articles according to relevance and credibility.
- Support for additional news providers.
- Streaming responses for faster user experience.
- Multi-language news retrieval and summarization.
- Personalized news recommendations.
- Cached search results for improved performance.
- User authentication and saved preferences.
- Topic subscriptions and notifications.
- Interactive conversational news assistant with follow-up questioning.
