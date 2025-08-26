from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from models import AgentState
from nodes import agent
from tools import retrieve_knowledge, tavily_search, get_card_by_name
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

tools = [retrieve_knowledge, tavily_search, get_card_by_name]
tool_node = ToolNode(tools)

def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    return END

workflow = StateGraph(AgentState)

workflow.add_node("agent", agent)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)

workflow.add_edge("tools", "agent")

graph = workflow.compile()


#If I attack with a deathtouch, trample 9/9 and the enemy blocks with a 1/5, how much damage does he take?
#What happens if I cast Murder on Serra Angel?
#If I give my Questing Beast trample and the attack with it and my opponent defends with Serra Angel, what happens?