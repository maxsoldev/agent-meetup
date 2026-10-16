# Agent Guild Meetups

Hands-on materials for Agent Guild meetups. Each numbered directory is a
self-contained workshop that builds a small agentic harness from first
principles.

## Workshops

- [1_agent_loop](1_agent_loop/README.md): LLM calls, tools, message history, token counts, and a command-line agent loop. Self-paced guide in [outline.md](1_agent_loop/docs/outline.md)
- [2_context_management](2_context_management/notes.md): context window anatomy, context rot, prompt caching, and context engineering (write, select, compress, isolate). Slides in [context-management-deck.pdf](2_context_management/materials/deck/context-management-deck.pdf)

## Reference harness

[educodex](https://github.com/maxsoldev/educodex) is an educational harness based on Codex. It shows every token the model receives, so you can see the context window from the talks in a real agent.

Each workshop uses `uv` for Python dependencies and requires an OpenRouter API
key for model calls.
