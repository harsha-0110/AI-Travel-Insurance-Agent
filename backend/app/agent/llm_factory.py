import os
import httpx
import requests
import urllib3
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from app.config import settings

# --- SSL Bypass Implementation ---
# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings()

# Globally bypass SSL verification for requests
session = requests.Session()
session.verify = False
requests.get = session.get

# Create an httpx client with SSL verification disabled for LangChain
ssl_bypass_client = httpx.Client(verify=False)
# ---------------------------------

def get_llm():

    if settings.LLM_PROVIDER == "openai":
        return ChatOpenAI(
            model="azure/genailab-maas-gpt-4o-mini",  # Change to "azure_ai/genailab-maas-DeepSeek-V3-0324" if using your office's custom model
            temperature=0,
            # Uncomment and set this if you are using your office's custom endpoint:
            base_url="https://genailab.tcs.in",
            api_key=settings.OPENAI_API_KEY, 
            http_client=ssl_bypass_client # Pass the custom client here
        )

    elif settings.LLM_PROVIDER == "ollama":
        return ChatOllama(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL,
            temperature=0
        )

    else:
        raise ValueError("Invalid LLM provider")