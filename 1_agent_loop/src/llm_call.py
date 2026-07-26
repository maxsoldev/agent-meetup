import json
import os
import urllib.request

from dotenv import load_dotenv

import typer

load_dotenv()

MODEL = "openai/gpt-5.6-luna"


def main(message: str) -> None:
    """Send one message to an LLM and print its reply."""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        typer.echo("Set OPENROUTER_API_KEY before running this command.", err=True)
        raise typer.Exit(code=1)

    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": message}],
    }
    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        reply = json.load(response)

    typer.echo(reply["choices"][0]["message"]["content"])


if __name__ == "__main__":
    # Run the following in terminal: 
    # uv run llm_call.py "What is an agentic coding harness?"
    typer.run(main)
