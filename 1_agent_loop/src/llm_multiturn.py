import json
import os
import urllib.request

from dotenv import load_dotenv

import typer
import tiktoken


load_dotenv()

MODEL = "openai/gpt-5.6-luna"
ENCODING = tiktoken.get_encoding("o200k_base")


def count_tokens(messages: list[dict]) -> int:
    return len(ENCODING.encode(json.dumps(messages)))


def count_text_tokens(text: str) -> int:
    return len(ENCODING.encode(text))


def chat(messages: list[dict]) -> dict:
    body = {"model": MODEL, "messages": messages}
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


def main() -> None:
    """Chat until the user types exit."""
    if not os.environ.get("OPENROUTER_API_KEY"):
        typer.echo("Set OPENROUTER_API_KEY in .env before running this command.", err=True)
        raise typer.Exit(code=1)

    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    while True:
        user_message = input("\nYou: ").strip()
        if user_message.lower() in {"exit", "quit"}:
            return
        if not user_message:
            continue

        messages.append({"role": "user", "content": user_message})
        token_count = count_tokens(messages)
        typer.echo(json.dumps(messages, indent=2))
        # typer.echo(f"\nMessages sent to the model (about {token_count} input tokens):")

        model_reply = chat(messages)
        answer = model_reply["content"]
        output_token_count = count_text_tokens(answer)
        typer.echo(f"\nAssistant: {answer}")
        # typer.echo(f"About {output_token_count} output tokens")
        messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    typer.run(main)
