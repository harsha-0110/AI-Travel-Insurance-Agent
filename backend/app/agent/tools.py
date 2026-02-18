from langchain.tools import Tool
from app.rag.retriever import get_retriever

retriever = get_retriever()

def retrieve_policy_info(query: str):
    docs = retriever.get_relevant_documents(query)
    return "\n\n".join([doc.page_content for doc in docs])


policy_tool = Tool(
    name="PolicyRetriever",
    func=retrieve_policy_info,
    description="Useful for answering questions about travel insurance policies, coverage and claims."
)
