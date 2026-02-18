from app.rag.vectorstore import create_vector_store

vectorstore = create_vector_store()

def get_retriever():
    return vectorstore.as_retriever(search_kwargs={"k": 4})
