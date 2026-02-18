from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import create_react_agent

from app.agent.llm_factory import get_llm
from app.agent.tools import policy_tool

# 1. Define the Graph State
class AgentState(TypedDict):
    # 'add_messages' ensures new messages are appended rather than overwritten
    messages: Annotated[list[BaseMessage], add_messages]
    next_step: str

def get_agent():
    llm = get_llm()

    # --------------------------------------------------
    # 2. Define the Specialized Worker Agents
    # --------------------------------------------------
    
    # Worker A: Policy Expert (Has access to the RAG vectorstore)
    policy_agent = create_react_agent(
        llm,
        tools=[policy_tool],
        prompt="You are an AI Travel Insurance Advisor. Use the PolicyRetriever tool to fetch specific coverage details, exclusions, and limits. Answer based strictly on the retrieved documents."
    )

    def policy_node(state: AgentState):
        # Run the agent and append its response to the state
        result = policy_agent.invoke({"messages": state["messages"]})
        return {"messages": [result["messages"][-1]]}

    # Worker B: Customer Support (Handles general chat without querying the DB)
    def support_node(state: AgentState):
        prompt = "You are a friendly customer support representative for a travel insurance company. Help the user with greetings, general inquiries, or direct them to ask about specific policies."
        response = llm.invoke([{"role": "system", "content": prompt}] + state["messages"])
        return {"messages": [response]}

    # --------------------------------------------------
    # 3. Define the Supervisor (Router)
    # --------------------------------------------------
    def supervisor_node(state: AgentState):
        last_message = state["messages"][-1].content
        
        # The supervisor analyzes the intent to decide the routing
        routing_prompt = f"""You are a routing supervisor for an insurance AI.
        Analyze the user's latest message: "{last_message}"
        
        If the message asks about insurance policies, coverage, limits, pricing, or claims, reply with EXACTLY the word "POLICY".
        If the message is a greeting (e.g., "hi", "hello"), casual chat, or general inquiry, reply with EXACTLY the word "SUPPORT".
        """
        
        response = llm.invoke(routing_prompt).content.strip().upper()
        
        # Set the next step based on the LLM's decision
        if "POLICY" in response:
            return {"next_step": "policy_expert"}
        else:
            return {"next_step": "support"}

    # --------------------------------------------------
    # 4. Build and Compile the Multi-Agent Graph
    # --------------------------------------------------
    workflow = StateGraph(AgentState)

    # Add agent nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("policy_expert", policy_node)
    workflow.add_node("support", support_node)

    # Start at the supervisor
    workflow.add_edge(START, "supervisor")

    # Add conditional routing logic from the supervisor
    workflow.add_conditional_edges(
        "supervisor",
        lambda state: state["next_step"],
        {
            "policy_expert": "policy_expert",
            "support": "support"
        }
    )

    # End the conversation after a worker agent replies
    workflow.add_edge("policy_expert", END)
    workflow.add_edge("support", END)

    # Compile the graph into an executable application
    return workflow.compile()