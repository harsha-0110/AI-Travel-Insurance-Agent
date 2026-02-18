from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from app.config import settings

def get_embeddings():

    if settings.LLM_PROVIDER == "openai":
        return OpenAIEmbeddings()

    else:
        return OllamaEmbeddings(model=settings.OLLAMA_MODEL)
