from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver  # <-- NEW: Import MemorySaver

from app.agent.llm_factory import get_llm
from app.agent.tools import policy_tool

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    next_step: str

def get_agent():
    llm = get_llm()

    policy_agent = create_react_agent(
        llm,
        tools=[policy_tool],
        prompt="You are an AI Travel Insurance Advisor. Use the PolicyRetriever tool to fetch specific coverage details, exclusions, and limits. Answer based strictly on the retrieved documents."
    )

    def policy_node(state: AgentState):
        result = policy_agent.invoke({"messages": state["messages"]})
        return {"messages": [result["messages"][-1]]}

    def support_node(state: AgentState):
        prompt = "You are a friendly customer support representative for a travel insurance company. Help the user with greetings, general inquiries, or direct them to ask about specific policies."
        response = llm.invoke([{"role": "system", "content": prompt}] + state["messages"])
        return {"messages": [response]}

    def supervisor_node(state: AgentState):
        last_message = state["messages"][-1].content
        
        routing_prompt = f"""You are a routing supervisor for an insurance AI.
        Analyze the user's latest message: "{last_message}"
        
        If the message asks about insurance policies, coverage, limits, pricing, or claims, reply with EXACTLY the word "POLICY".
        If the message is a greeting (e.g., "hi", "hello"), casual chat, or general inquiry, reply with EXACTLY the word "SUPPORT".
        """
        
        response = llm.invoke(routing_prompt).content.strip().upper()
        
        if "POLICY" in response:
            return {"next_step": "policy_expert"}
        else:
            return {"next_step": "support"}

    workflow = StateGraph(AgentState)

    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("policy_expert", policy_node)
    workflow.add_node("support", support_node)

    workflow.add_edge(START, "supervisor")
    workflow.add_conditional_edges(
        "supervisor",
        lambda state: state["next_step"],
        {
            "policy_expert": "policy_expert",
            "support": "support"
        }
    )
    workflow.add_edge("policy_expert", END)
    workflow.add_edge("support", END)

    # --- NEW: Initialize memory and add it to the compiled graph ---
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)