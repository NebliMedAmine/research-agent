from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent.graph import research_graph
from langchain_core.messages import HumanMessage, AIMessage

app = FastAPI(title="ResearchAgent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    history: list = []

class QueryResponse(BaseModel):
    answer: str
    route: str = ""
    status: str = "success"

@app.get("/")
def root():
    return {"message": "ResearchAgent API is running"}

@app.post("/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    try:
        messages = []
        for h in request.history:
            if h["role"] == "user":
                messages.append(HumanMessage(content=h["content"]))
            elif h["role"] == "agent":
                messages.append(AIMessage(content=h["content"]))

        result = research_graph.invoke({
            "query": request.query,
            "messages": messages,
            "route": "",
            "specialist_output": "",
            "final_answer": "",
            "search_iterations": 0,
            "sufficient": False
        })

        return QueryResponse(
            answer=result["final_answer"],
            route=result["route"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy"}