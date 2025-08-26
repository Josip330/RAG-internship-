from models import AgentState
from config import get_llm
from tools import retrieve_knowledge, tavily_search, get_card_by_name
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage, AIMessage, ToolMessage

llm = get_llm()
tools = {
    "retrieve_knowledge": retrieve_knowledge,
    "tavily_search": tavily_search,
    "get_card_by_name": get_card_by_name,
}
llm_with_tools = llm.bind_tools(list(tools.values()))


def agent(state: AgentState):
    messages = state["messages"]

    # Add system prompt
    system_prompt = SystemMessage(
        content=(
            "You are a helpful Magic: The Gathering judge. "
            "You have access to multiple tools: "
            "- retrieve_knowledge (searches MTG rules database), "
            "- tavily_search (searches the internet), "
            "- get_card_by_name (retrieves card information by name).\n\n"
            "You may want to fetch card information before querying the rules and formulating a query for the rules based on the results of that fetch,"
            "but use the tools as you see fit."
        )
    )

    # Prepend the system message
    full_messages = [system_prompt] + messages

    ai_response = llm_with_tools.invoke(full_messages)

    updated_messages = messages + [ai_response]
    new_state = {
        "messages": updated_messages,
        "rules_info": state.get("rules_info"),
        "cards_info": state.get("cards_info"),
        "search_info": state.get("search_info"),
    }

    if isinstance(ai_response, AIMessage) and ai_response.tool_calls:
        for tool_call in ai_response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call.get("args", {})

            if tool_name in tools:
                result = tools[tool_name].invoke(tool_args)

                # Save tool result
                if tool_name == "retrieve_knowledge":
                    new_state["rules_info"] = result
                elif tool_name == "get_card_by_name":
                    if new_state["cards_info"] is None:
                        new_state["cards_info"] = []
                    new_state["cards_info"].append(result)
                elif tool_name == "tavily_search":
                    new_state["search_info"] = result

                # Add tool response to messages
                updated_messages.append(
                    ToolMessage(
                        tool_call_id=tool_call["id"],
                        content=result
                    )
                )

        # Re-assign updated messages with tools to state
        new_state["messages"] = updated_messages

    return new_state


