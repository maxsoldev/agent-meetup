import json
import os
import urllib.parse
import urllib.request

from dotenv import load_dotenv

import typer


load_dotenv()

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


def get_json(url: str, parameters: dict) -> dict:
    query = urllib.parse.urlencode(parameters)
    with urllib.request.urlopen(f"{url}?{query}") as response:
        return json.load(response)


def get_weather(city: str) -> dict:
    places = get_json(
        "https://geocoding-api.open-meteo.com/v1/search",
        {"name": city, "count": 1, "language": "en", "format": "json"},
    )
    if not places.get("results"):
        raise ValueError(f"Could not find {city!r}.")

    place = places["results"][0]
    forecast = get_json(
        "https://api.open-meteo.com/v1/forecast",
        {
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "current": "temperature_2m,apparent_temperature,precipitation,wind_speed_10m",
        },
    )
    current = forecast["current"]
    return {
        "city": place["name"],
        "country": place.get("country"),
        "temperature_c": current["temperature_2m"],
        "feels_like_c": current["apparent_temperature"],
        "precipitation_mm": current["precipitation"],
        "wind_speed_kmh": current["wind_speed_10m"],
    }


def llm_call(messages: list[dict]) -> dict:
    body = {"model": MODEL, "messages": messages, "tools": [WEATHER_TOOL]}
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


def main(message: str) -> None:
    """Answer a question, using the weather API when the model asks for it."""
    if not os.environ.get("OPENROUTER_API_KEY"):
        typer.echo("Set OPENROUTER_API_KEY in .env before running this command.", err=True)
        raise typer.Exit(code=1)

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
    if tool_call["function"]["name"] != "get_weather":
        raise ValueError("The model requested an unknown tool.")
    arguments = json.loads(tool_call["function"]["arguments"])
    typer.echo(f"Tool call: get_weather({arguments['city']!r})", err=True)
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
    # typer.echo(chat(messages)["content"])


if __name__ == "__main__":
    typer.run(main)
