import json
import os
import urllib.request

from dotenv import load_dotenv

import typer
import tiktoken


load_dotenv()

MODEL = "openai/gpt-5.6-luna"
ENCODING = tiktoken.get_encoding("o200k_base")
API_KEY = os.environ['OPENROUTER_API_KEY']
assert API_KEY, "Set OPENROUTER_API_KEY in .env file before running this command."


def count_tokens(messages: list[dict]) -> int:
    return len(ENCODING.encode(json.dumps(messages)))


def count_text_tokens(text: str) -> int:
    return len(ENCODING.encode(text))


def llm_call(messages: list[dict]) -> dict:
    body = {"model": MODEL, "messages": messages, "tools": []}

    typer.echo("\n#### LLM Sees: ####")
    typer.echo(json.dumps(messages, indent=2))

    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        reply = json.load(response)["choices"][0]["message"]

    typer.echo("\n#### LLM Does: ####")
    typer.echo(json.dumps(reply, indent=2))
    return reply


def main() -> None:
    """Chat until the user types exit."""
    messages = []  # [{"role": "system", "content": "You must always respond like a pirate"}]

    while True:
        user_message = input("\nYou: ").strip()
        if user_message.lower() in {"exit", "quit"}:
            return
        if not user_message:
            continue

        messages.append({"role": "user", "content": user_message})
        typer.echo(json.dumps(messages, indent=2))
        # token_count = count_tokens(messages)
        # typer.echo(f"\nMessages sent to the model (about {token_count} input tokens):")

        model_reply = llm_call(messages)
        answer = model_reply["content"]
        typer.echo(f"\nAssistant: {answer}")
        # output_token_count = count_text_tokens(answer)
        # typer.echo(f"About {output_token_count} output tokens")
        messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    typer.run(main)
