from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from typing import TypedDict, List, Annotated, Optional
import operator

class AgentState(TypedDict):
    messages: Annotated[List[HumanMessage | AIMessage | ToolMessage], operator.add]
    rules_info: Optional[str] = None
    cards_info: Optional[List[str]]
    search_info: Optional[str] = None

