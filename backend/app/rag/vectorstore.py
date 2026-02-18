from langchain_community.vectorstores import FAISS
from app.rag.loader import load_policy_documents
from app.rag.embeddings import get_embeddings

def create_vector_store():

    docs = load_policy_documents()
    embeddings = get_embeddings()

    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore
