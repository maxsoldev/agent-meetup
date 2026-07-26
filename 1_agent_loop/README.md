# Agent Loop

This workshop builds an agentic coding harness step by step: a simple LLM
call, tool calling, message history, token counting, and a command-line agent.

## Setup

From the repository root, install [`uv`](https://docs.astral.sh/uv/) if needed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Create the local environment file and add an OpenRouter API key:

```bash
cp .env.example .env
```

```dotenv
OPENROUTER_API_KEY="your-api-key"
```

Install the workshop dependencies:

```bash
cd 1_agent_loop
uv sync
```

## Run The Examples

```bash
# One LLM request
uv run python src/llm_call.py "What is a coding harness?"

# LLM tool calling with current weather
uv run python src/llm_tool_call.py "What is the weather in Munich right now?"

# Multi-turn chat with visible message history
uv run python src/llm_multiturn.py

# A command-line agent that asks before running each Bash command
uv run python src/simple_agent.py "List the Python files in src."

# The same agent with persistent conversation history
uv run python src/simple_agent_interactive.py
```

The agent examples can run commands with your user permissions. Review every
command before confirming it.
