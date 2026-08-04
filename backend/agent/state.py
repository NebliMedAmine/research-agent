from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    query: str
    messages: Annotated[List[BaseMessage], operator.add]
    route: str
    specialist_output: str
    final_answer: str
    search_iterations: int
    sufficient: bool