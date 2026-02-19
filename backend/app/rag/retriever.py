from app.rag.vectorstore import create_vector_store

vectorstore = create_vector_store()

def get_retriever():
    # Use MMR for diversity across documents and increase the number of chunks retrieved (k)
    return vectorstore.as_retriever(
        search_type="mmr", 
        search_kwargs={
            "k": 15,         # Number of final documents to return to the LLM
            "fetch_k": 50    # Number of documents to fetch initially before filtering for diversity
        }
    )