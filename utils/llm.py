import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


# Load environment variables
load_dotenv()


# Get Groq API Key
GROQ_API_KEY = os.getenv("LLM_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")


# Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=GROQ_API_KEY
)