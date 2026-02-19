import httpx
import requests
import urllib3
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
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

def get_embeddings():

    if settings.LLM_PROVIDER == "openai":
        return OpenAIEmbeddings(
            base_url="https://genailab.tcs.in",
            model="azure/genailab-maas-text-embedding-3-large", # Explicitly set the embedding model
            api_key=settings.OPENAI_API_KEY, # Make sure this is set to your 'KEY' in the .env file
            http_client=ssl_bypass_client
        )

    else:
        return OllamaEmbeddings(
            model=settings.OLLAMA_MODEL
        )