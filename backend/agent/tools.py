# backend/agent/tools.py

from langchain_tavily import TavilySearch
from langchain_experimental.tools import PythonREPLTool
from dotenv import load_dotenv

load_dotenv()

# ── 1. Web Search Tool ────────────────────────────────────────────────────────
web_search_tool = TavilySearch(
    max_results=5,
    description=(
        "Use this tool to search the web for current information, recent events, "
        "statistics, or any question that requires up-to-date data. "
        "Input should be a clear, specific search query."
    )
)

# ── 2. Python REPL Tool ───────────────────────────────────────────────────────
python_repl_tool = PythonREPLTool(
    description=(
        "Use this tool to execute Python code. Useful for math calculations, "
        "data analysis, generating charts with matplotlib, or any computation. "
        "Input should be valid Python code. Always print your results."
    )
)

def get_base_tools():
    return [web_search_tool, python_repl_tool]