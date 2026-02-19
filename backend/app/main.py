from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from app.agent.agent_executor import get_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = get_agent()

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default-session"  # <-- NEW: Added session tracking

@app.post("/chat")
def chat(req: ChatRequest):
    print(f"User Message: {req.message} | Session: {req.session_id}")
    
    # --- NEW: Create a config dict with the thread_id (session) ---
    config = {"configurable": {"thread_id": req.session_id}}
    
    # Pass the config to invoke() so LangGraph loads/saves the correct history
    result = agent.invoke(
        {"messages": [HumanMessage(content=req.message)]}, 
        config=config
    )
    
    final_message = result["messages"][-1].content
    
    return {"response": final_message}