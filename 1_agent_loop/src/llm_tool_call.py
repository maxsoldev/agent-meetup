import json
import os
import urllib.parse
import urllib.request

from dotenv import load_dotenv

import typer


load_dotenv()

if not os.environ.get("OPENROUTER_API_KEY"):
    typer.echo("Set OPENROUTER_API_KEY in .env before running this command.", err=True)
    raise typer.Exit(code=1)

MODEL = "openai/gpt-5.6-luna"

WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city to look up, for example Munich.",
                }
            },
            "required": ["city"],
        },
    },
}


def get_weather(city: str) -> dict:
    url = f"https://wttr.in/{urllib.parse.quote(city, safe='')}?format=j1"
    with urllib.request.urlopen(url) as response:
        weather = json.load(response)

    current = weather["current_condition"][0]
    return {
        "city": city,
        "temperature_c": current["temp_C"],
        "feels_like_c": current["FeelsLikeC"],
        "description": current["weatherDesc"][0]["value"],
        "wind_speed_kmh": current["windspeedKmph"],
    }


def llm_call(messages: list[dict]) -> dict:
    body = {"model": MODEL, "messages": messages, "tools": [WEATHER_TOOL]}

    typer.echo("\n#### LLM Sees: ####")
    typer.echo(json.dumps(messages, indent=2))

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
        reply = json.load(response)["choices"][0]["message"]

    typer.echo("\n#### LLM Does: ####")
    typer.echo(json.dumps(reply, indent=2))
    return reply


def main(message: str) -> None:
    """Answer a question, using the weather API when the model asks for it."""

    messages = [
        {"role": "user", "content": message},
    ]

    # 1. The model decides whether it needs the tool.
    model_reply = llm_call(messages)
    tool_calls = model_reply.get("tool_calls") or []
    if not tool_calls:
        typer.echo(model_reply.get("content", "The model did not request a tool."))
        return

    # 2. Our code runs the tool requested by the model.
    tool_call = tool_calls[0]
    # parse the tool call
    arguments = json.loads(tool_call["function"]["arguments"])
    typer.echo(f"Tool call: get_weather({arguments['city']!r})", err=True)
    # call the weather function with tool call arguments
    weather = get_weather(arguments["city"])
    typer.echo(f"Tool result: {json.dumps(weather)}", err=True)

    # 3. Give the tool result to the model so it can answer the user.
    # messages.append(model_reply)
    # messages.append(
    #     {
    #         "role": "tool",
    #         "tool_call_id": tool_call["id"],
    #         "content": json.dumps(weather),
    #     }
    # )
    # typer.echo(llm_call(messages)["content"])


if __name__ == "__main__":
    typer.run(main)
