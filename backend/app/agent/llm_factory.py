from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from app.config import settings

def get_llm():

    if settings.LLM_PROVIDER == "openai":
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )

    elif settings.LLM_PROVIDER == "ollama":
        return ChatOllama(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL,
            temperature=0
        )

    else:
        raise ValueError("Invalid LLM provider")
