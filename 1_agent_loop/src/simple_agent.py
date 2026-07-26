import json
import os
import subprocess
import urllib.request

from dotenv import load_dotenv

import typer


load_dotenv()

MODEL = "openai/gpt-5.6-luna"
MAX_TURNS = 10

BASH_TOOL = {
    "type": "function",
    "function": {
        "name": "run_bash",
        "description": "Run a Bash command on the local computer and return its output.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The Bash command to run.",
                }
            },
            "required": ["command"],
        },
    },
}


def run_bash(command: str) -> str:
    typer.echo(f"\nTool call: run_bash({command!r})", err=True)
    if input("Run this command? [y/N] ").strip().lower() != "y":
        return "The user declined to run this command."

    try:
        result = subprocess.run(
            command,
            shell=True,
            executable="/bin/bash",
            text=True,
            capture_output=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        return "The command timed out after 30 seconds."

    tool_result = {
        "exit_code": result.returncode,
        "stdout": result.stdout[-4000:],
        "stderr": result.stderr[-4000:],
    }
    output = tool_result["stdout"] or tool_result["stderr"] or "(no output)"
    typer.echo(f"Tool result (exit code {result.returncode}):\n{output}", err=True)
    return json.dumps(tool_result)


def llm_call(messages: list[dict]) -> dict:
    body = {"model": MODEL, "messages": messages, "tools": [BASH_TOOL]}
    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        reply = json.load(response)
    return reply["choices"][0]["message"]


def main(task: str) -> None:
    """Use Bash commands to complete a task."""
    if not os.environ.get("OPENROUTER_API_KEY"):
        typer.echo("Set OPENROUTER_API_KEY in .env before running this command.", err=True)
        raise typer.Exit(code=1)

    messages = [
        {
            "role": "system",
            "content": "You are a command-line agent. Use run_bash to complete the user's task.",
        },
        {"role": "user", "content": task},
    ]

    for _ in range(MAX_TURNS):
        model_reply = llm_call(messages)
        messages.append(model_reply)

        tool_calls = model_reply.get("tool_calls") or []
        if not tool_calls:
            typer.echo(model_reply.get("content", "The agent finished."))
            return

        for tool_call in tool_calls:
            if tool_call["function"]["name"] != "run_bash":
                tool_result = "The model requested an unknown tool."
            else:
                arguments = json.loads(tool_call["function"]["arguments"])
                tool_result = run_bash(arguments["command"])

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": tool_result,
                }
            )

    typer.echo(f"Stopped after {MAX_TURNS} tool turns.", err=True)


if __name__ == "__main__":
    typer.run(main)
