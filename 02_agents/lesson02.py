import json
import os

import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def get_latest_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather of the {city.title()} is {response.text}"
    else:
        return None

# print(get_latest_weather("goa"))
response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {   "role": "system",
            "content": "You are a helpful AI assistant"
        },
        {
            "role": "user",
            "content": "What is weather in Goa"
        }
    ],
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message
if message.content is not None:
    print(message.content)

tool_calls = message.tool_calls
if tool_calls:
    tool_call = tool_calls[0]

    args = json.loads(tool_call.function.arguments)

    result = get_latest_weather(args["city"])

    print("Tool Result:", result)