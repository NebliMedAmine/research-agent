from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from .tools import web_search_tool, python_repl_tool

llm = ChatOpenAI(model="gpt-4o", temperature=0)

web_agent = create_react_agent(
    model=llm,
    tools=[web_search_tool],
    prompt="""You are a web research specialist. Your only job is to search 
the web and return accurate, well-sourced information. Always cite your sources.
Be thorough but concise. Never fabricate information."""
)

code_agent = create_react_agent(
    model=llm,
    tools=[python_repl_tool],
    prompt="""You are a code execution specialist. Your job is to write and run 
Python code to answer questions. Always print your results clearly.
For charts, use matplotlib. Explain what your code does and what the output means."""
)

general_llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

def run_general(query: str, history: list) -> str:
    messages = history + [HumanMessage(content=query)]
    result = general_llm.invoke(messages)
    return result.content

def run_web_agent(query: str, history: list) -> str:
    messages = history + [HumanMessage(content=query)]
    result = web_agent.invoke({"messages": messages})
    return result["messages"][-1].content

def run_code_agent(query: str, history: list) -> str:
    messages = history + [HumanMessage(content=query)]
    result = code_agent.invoke({"messages": messages})
    return result["messages"][-1].content