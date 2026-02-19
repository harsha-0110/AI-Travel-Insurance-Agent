from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.rag.loader import load_policy_documents
from app.rag.embeddings import get_embeddings

def create_vector_store():
    # 1. Load the raw PDF documents
    raw_docs = load_policy_documents()
    
    # 2. Split the documents into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150,
        length_function=len
    )
    chunks = text_splitter.split_documents(raw_docs)

    # 3. Create embeddings and store them in FAISS
    embeddings = get_embeddings()
    
    # Handle the case where the policies folder is empty
    if not chunks:
        print("No documents found to index.")
        return None

    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore