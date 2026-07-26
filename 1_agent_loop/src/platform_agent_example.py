#!/usr/bin/env python3
"""
Standalone agent, compiled from Agent Builder agent "New Agent".
Behavior mirrors mobile-agent-builder's in-browser runtime: same tools, system prompt, and turn loop.
Run outside the browser via an AFC API key. Uses only the Python standard library.

Pinned to one competition + scenario — edit COMPETITION_ID / SCENARIO_ID below
to play a different one.
"""


import json
import os
import sys
import urllib.error
import urllib.request


def _load_dotenv():
    """Loads KEY=VALUE pairs from a .env file next to this script, without
    overriding variables already set in the environment."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_dotenv()


AFC_SERVER_URL = os.environ.get("AFC_SERVER_URL") or "https://agentfightclub.today"
AFC_API_KEY = os.environ.get("AFC_API_KEY")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

COMPETITION_ID = "c28e65b9-f470-4c9f-9e55-0d12d25f8378"
SCENARIO_ID = "l4_sand_temple_2_4x4"

AGENT_NAME = "New Agent"
MODEL = "google/gemini-3-flash-preview"
INSTRUCTIONS = "Dank agent"
MAX_TOKENS = 1024
MAX_TURNS = 120


def _log(label, text):
    print(f"[{label}] {text}")
    sys.stdout.flush()


def _http(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Authorization": f"Bearer {AFC_API_KEY}"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(f"{AFC_SERVER_URL}{path}", data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            text = resp.read().decode()
    except urllib.error.HTTPError as exc:
        text = exc.read().decode()
        message = text or str(exc)
        try:
            parsed = json.loads(text)
            if isinstance(parsed, dict) and "message" in parsed:
                message = parsed["message"]
        except json.JSONDecodeError:
            pass
        raise RuntimeError(f"{method} {path} -> {exc.code}: {message}") from exc
    return json.loads(text) if text else None


def _run_game_command(path, command_str):
    parts = (command_str or "").strip().split()
    cmd = parts[0] if parts else ""
    args = parts[1:]
    result = _http("POST", path, {"command": cmd, "args": args})
    return result.get("message") if isinstance(result, dict) and result.get("message") else json.dumps(result)


def _chat_completion(messages, tools):
    body = {"model": MODEL, "messages": messages, "usage": {"include": True}}
    if tools:
        body["tools"] = tools
    if MAX_TOKENS:
        body["max_tokens"] = MAX_TOKENS

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            payload = json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"OpenRouter API error ({exc.code}): {exc.read().decode()}") from exc

    if payload.get("error"):
        raise RuntimeError(f"OpenRouter error: {payload['error'].get('message')}")

    choices = payload.get("choices") or []
    if not choices:
        raise RuntimeError("No response from model")

    message = choices[0]["message"]
    return {
        "content": message.get("content"),
        "tool_calls": message.get("tool_calls"),
        "finish_reason": choices[0].get("finish_reason"),
    }


MAIN_AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "game_command",
            "description": "Execute a command in the current game.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to execute in the game",
                    },
                },
                "required": [
                    "command",
                ],
            },
        },
    },
]


def run_main_agent():
    _log(AGENT_NAME, f"Starting agent with model {MODEL}...")

    game = _http("POST", f"/escapegames/api/competitions/{COMPETITION_ID}/games", {"scenarioId": SCENARIO_ID, "context": "agent-builder"})
    game_id = game["gameId"]
    _log(AGENT_NAME, f"Game created: {game_id}")
    _log(AGENT_NAME, f"Live map: {AFC_SERVER_URL}/escapegames/ui/competitions/{COMPETITION_ID}/games/{game_id}/livemap")

    start_result = _http("POST", f"/escapegames/api/competitions/{COMPETITION_ID}/games/{game_id}/command", {"command": "start"})
    _log(AGENT_NAME, f"Game started: {(start_result or {}).get('message', 'OK')}")

    path = f"/escapegames/api/competitions/{COMPETITION_ID}/games/{game_id}/command"
    messages = [
        {"role": "system", "content": INSTRUCTIONS},
        {"role": "user", "content": "Follow the system prompt."},
    ]

    turn_count = 0
    while turn_count < MAX_TURNS:
        turn_count += 1
        _log(AGENT_NAME, f"Turn {turn_count}/{MAX_TURNS} — thinking...")
        response = _chat_completion(messages, MAIN_AGENT_TOOLS)

        if response["content"]:
            _log(AGENT_NAME, response["content"])

        tool_calls = response.get("tool_calls")
        if not tool_calls:
            if response.get("finish_reason") == "length":
                _log(AGENT_NAME, f"Model hit max_tokens ({MAX_TOKENS}) before calling a tool. Raise MAX_TOKENS.")
            break

        messages.append({"role": "assistant", "content": response["content"], "tool_calls": tool_calls})

        for tool_call in tool_calls:
            args = json.loads(tool_call["function"]["arguments"])
            _log(AGENT_NAME, f"{tool_call['function']['name']}({tool_call['function']['arguments']})")
            try:
                result = _run_game_command(path, args.get("command"))
            except Exception as exc:
                result = f"Error: {exc}"
            messages.append({"role": "tool", "tool_call_id": tool_call["id"], "content": result})

    if turn_count >= MAX_TURNS:
        _log(AGENT_NAME, f"Turn limit reached ({MAX_TURNS}). Agent stopped.")

    try:
        stats = _http("GET", f"/escapegames/api/games/{game_id}/stats")
        if stats:
            total_seconds = (stats.get("timeSpentMs") or 0) // 1000
            minutes, seconds = divmod(total_seconds, 60)
            time_str = f"{minutes}m {seconds}s" if minutes else f"{seconds}s"
            status = stats.get("status")
            outcome = "Won" if status == "completed" else "Failed" if status == "failed" else status
            _log(AGENT_NAME, f"Game {outcome} — {stats.get('turnCount')} turns, {time_str}")
    except Exception:
        pass

    _log(AGENT_NAME, "Agent finished.")


if __name__ == "__main__":
    if not AFC_API_KEY:
        print(f"[{AGENT_NAME}] error: AFC_API_KEY env var required. See env.sample.", file=sys.stderr)
        sys.exit(1)
    if not OPENROUTER_API_KEY:
        print(f"[{AGENT_NAME}] error: OPENROUTER_API_KEY env var required. See env.sample.", file=sys.stderr)
        sys.exit(1)

    try:
        run_main_agent()
    except Exception as exc:
        print(f"[{AGENT_NAME}] error: {exc}", file=sys.stderr)
        sys.exit(1)
