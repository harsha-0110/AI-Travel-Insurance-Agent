from langchain_classic.chains import RetrievalQA

from langchain_core.prompts import ChatPromptTemplate
from app.agent.llm_factory import get_llm
from app.rag.retriever import get_retriever

def get_agent():

    llm = get_llm()
    retriever = get_retriever()

    prompt = ChatPromptTemplate.from_template("""
You are an AI Travel Insurance Advisor.

Use the provided policy context to answer the question clearly.
Provide personalized explanations and compare plans when necessary.

Context:
{context}

Question:
{question}

Answer:
""")

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )

    return qa_chain
