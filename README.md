# AI-Agents-Hackathon

Hugging Face Hackathon

Restaurant Caller and Booker.

# 🍽️ Paris Restaurant Booker — Agentic Voice Assistant

This is a voice-powered AI agent that helps users **find and book restaurants in Paris** based on their preferences (e.g., cuisine type, location, weather). Built during a hackathon to showcase **agentic reasoning**, real-time **tool use**, and a natural conversation interface.

---

## 🧠 How It Works

We use an **LLM agent (Claude 3 Sonnet)** that dynamically:
- Asks clarifying questions ("What cuisine do you prefer?")
- Calls external tools to gather context (e.g., weather, restaurant options)
- Returns structured, conversational answers
- Continues the conversation based on user intent

The full loop is built using **LangGraph** to handle stateful reasoning and **LiteLLM** to route messages through Claude.

---

## 🔧 Tools Used by the Agent

| Tool | Description |
|------|-------------|
| `get_weather_info(location)` | Returns a summary of current weather (for indoor/outdoor seating recommendation). |
| `search_restaurants(term, location)` | Searches for the best-rated nearby places by keyword (e.g., "sushi", "Italian"). |
| `get_restaurant_details(place_id)` | (Optional) Fetches more details about a specific restaurant. |

Each tool is triggered **only when needed**, using structured tool calls from Claude.

---

## 💡 Key Agentic Components

- **LLM + Tools Binding**: We use Claude 3 Sonnet via LiteLLM and explicitly bind tools for invocation.
- **Tool Routing Logic**: LangGraph monitors tool calls and prevents repeated execution using `tool_call_id`.
- **State Management**: A custom `AgentState` tracks the full message history to maintain context.
- **Autonomous Reasoning**: Claude decides which tools to call, when, and how to continue after.

---

## 🚀 Run Locally

```bash
# Setup environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your keys

# Start the server
python main.py
