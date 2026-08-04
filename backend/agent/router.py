from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0)

ROUTER_PROMPT = """You are a routing agent. Your job is to read the user's query 
and decide which specialist agent should handle it.

Your options:
- "web" — for current events, news, recent facts, real-time data, anything 
   that requires up-to-date information from the internet
- "code" — for math calculations, data analysis, chart generation, 
   programming questions, anything requiring code execution
- "general" — for general knowledge, explanations, reasoning, 
   summaries, opinions, anything that doesn't need tools

Reply with ONLY one word: web, code, or general.
Nothing else. No explanation.

User query: {query}
"""

prompt = ChatPromptTemplate.from_template(ROUTER_PROMPT)
router_chain = prompt | llm

def route_query(query: str) -> str:
    result = router_chain.invoke({"query": query})
    route = result.content.strip().lower()
    if route not in ["web", "code", "general"]:
        return "general"
    return route