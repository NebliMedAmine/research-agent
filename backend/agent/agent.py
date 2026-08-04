from langchain_core.messages import HumanMessage, AIMessage
from .graph import research_graph

def run_agent(user_input: str, history: list = []) -> str:
    messages = []
    for h in history:
        if h["role"] == "user":
            messages.append(HumanMessage(content=h["content"]))
        elif h["role"] == "agent":
            messages.append(AIMessage(content=h["content"]))

    result = research_graph.invoke({
        "query": user_input,
        "messages": messages,
        "route": "",
        "specialist_output": "",
        "final_answer": "",
        "search_iterations": 0,
        "sufficient": False
    })

    return result["final_answer"], result["route"]