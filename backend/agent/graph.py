import json
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from .state import AgentState
from .router import route_query
from .specialisits import run_web_agent, run_code_agent, run_general

llm = ChatOpenAI(model="gpt-4o", temperature=0)

# ── Node: Router ──────────────────────────────────────────────────────────────
def router_node(state: AgentState) -> AgentState:
    route = route_query(state["query"])
    return {**state, "route": route}

# ── Node: Web Researcher ──────────────────────────────────────────────────────
def web_node(state: AgentState) -> AgentState:
    output = run_web_agent(state["query"], state["messages"])
    return {**state, "specialist_output": output}

# ── Node: Code Analyst ────────────────────────────────────────────────────────
def code_node(state: AgentState) -> AgentState:
    output = run_code_agent(state["query"], state["messages"])
    return {**state, "specialist_output": output}

# ── Node: General ─────────────────────────────────────────────────────────────
def general_node(state: AgentState) -> AgentState:
    output = run_general(state["query"], state["messages"])
    return {**state, "specialist_output": output}

# ── Node: Quality Checker ─────────────────────────────────────────────────────
def quality_check_node(state: AgentState) -> AgentState:
    prompt = f"""You are a research quality checker.

A web researcher just returned this output for the query: "{state["query"]}"

Output: {state["specialist_output"]}

Is this output sufficient to fully answer the user's question?
Consider:
- Does it directly address the question?
- Is there enough detail?
- Are there clear gaps or unanswered parts?

Reply with ONLY a JSON object, no markdown, no backticks:
{{"sufficient": true/false, "reason": "one sentence explanation", "followup_query": "refined search query if not sufficient"}}
"""
    result = llm.invoke(prompt)

    try:
        parsed = json.loads(result.content.strip())
        sufficient = parsed.get("sufficient", True)
        followup = parsed.get("followup_query", state["query"])
    except:
        sufficient = True
        followup = state["query"]

    return {
        **state,
        "sufficient": sufficient,
        "query": followup if not sufficient else state["query"],
        "search_iterations": state.get("search_iterations", 0) + 1
    }

# ── Node: Synthesizer ─────────────────────────────────────────────────────────
def synthesizer_node(state: AgentState) -> AgentState:
    prompt = f"""You are a response synthesizer.
A specialist agent has already done the research. Your job is to take their 
output and write a clean, well-structured final answer for the user.

Original question: {state["query"]}
Specialist output: {state["specialist_output"]}
Agent used: {state["route"]}

Write the final answer clearly. Preserve any sources or citations.
Do not add information that isn't in the specialist output."""

    result = llm.invoke(prompt)
    return {**state, "final_answer": result.content}

# ── Routing conditions ────────────────────────────────────────────────────────
def decide_route(state: AgentState) -> str:
    return state["route"]

def should_continue_search(state: AgentState) -> str:
    if state["search_iterations"] >= 3:
        return "synthesize"
    if state["sufficient"]:
        return "synthesize"
    return "search_again"

# ── Build the graph ───────────────────────────────────────────────────────────
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", router_node)
    graph.add_node("web", web_node)
    graph.add_node("code", code_node)
    graph.add_node("general", general_node)
    graph.add_node("quality_check", quality_check_node)
    graph.add_node("synthesizer", synthesizer_node)

    graph.set_entry_point("router")

    graph.add_conditional_edges(
        "router",
        decide_route,
        {
            "web": "web",
            "code": "code",
            "general": "general"
        }
    )

    graph.add_edge("web", "quality_check")

    graph.add_conditional_edges(
        "quality_check",
        should_continue_search,
        {
            "search_again": "web",
            "synthesize": "synthesizer"
        }
    )

    graph.add_edge("code", "synthesizer")
    graph.add_edge("general", "synthesizer")
    graph.add_edge("synthesizer", END)

    return graph.compile()

research_graph = build_graph()