from fastapi import FastAPI, Depends
from app.agent.agent_executor import get_agent
from pydantic import BaseModel

app = FastAPI()

agent = get_agent()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    print(req.message)
    result = agent.invoke({"query": req.message})
    return {"response": result["result"]}

    
