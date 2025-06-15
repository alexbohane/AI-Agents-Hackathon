from typing import TypedDict, Annotated, Optional, List
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_litellm import ChatLiteLLM
from dotenv import load_dotenv
import json

# Tool + Prompt imports
from prompt_config import system_prompt
from tools import get_weather_info, search_restaurants, get_restaurant_details

# Load environment variables
load_dotenv()

# Tool setup
TOOLS = [get_weather_info, search_restaurants, get_restaurant_details]

# Claude model via LiteLLM
llm = ChatLiteLLM(
    model="anthropic/claude-3-7-sonnet-20250219",
    temperature=0.3
)
llm_with_tools = llm.bind_tools(TOOLS)

# --- Agent State Definition ---
class AgentState(TypedDict):
    messages: Annotated[List[SystemMessage | HumanMessage | AIMessage], add_messages]
    last_user_prompt: Optional[str]

# --- Tool Handler ---
def handle_tool_calls(messages: List, tool_calls: List) -> AIMessage:
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)
        tool_id = tool_call.id

        print(f"🛠️ Invoking tool: {tool_name} with args {tool_args}")

        for tool in TOOLS:
            if tool.name == tool_name:
                output = tool.invoke(tool_args)
                break
        else:
            output = f"Tool '{tool_name}' not found."

        messages.append(ToolMessage(tool_call_id=tool_id, content=str(output)))

    followup = llm_with_tools.invoke(messages)
    print("🧠 Final assistant response:", followup.content)
    return followup

# --- LangGraph Node ---
def generate_response(state: AgentState) -> AgentState:
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    print("🤖 Claude responded:", response)

    messages.append(response)

    tool_calls = response.additional_kwargs.get("tool_calls", [])
    if tool_calls:
        followup = handle_tool_calls(messages, tool_calls)
        messages.append(followup)

    state["messages"] = messages
    return state

# --- LangGraph Agent Assembly ---
def get_langgraph_agent():
    builder = StateGraph(AgentState)
    builder.add_node("respond", generate_response)
    builder.set_entry_point("respond")
    builder.set_finish_point("respond")
    return builder.compile()

graph = get_langgraph_agent()

# --- External Interface ---
async def run_agent(conversation: List[dict]) -> str:
    messages = []
    for msg in conversation:
        if msg["role"] == "system":
            messages.append(SystemMessage(content=msg["content"]))
        elif msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))

    inputs = {"messages": messages}
    final_state = graph.invoke(inputs)
    return final_state["messages"][-1].content
