from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import (HumanMessage,ToolMessage)

import os

llm = ChatOpenAI(model="gpt-4o-mini",api_key=os.getenv("OPENAI_API_KEY"))

@tool
def get_weather(city:str)->str:
    """Get weather of a city."""
    # fake/mock weather data
    weather_data={
        "peshawar": "35°C Sunny",

        "karachi": "30°C Humid",

        "london": "15°C Rainy"
    }

    return weather_data.get(city.lower(),"weather not found")

@tool
def suggest_clothes(weather:str)->str:
    """Suggest clothes based on weather"""

    if "Sunny" in weather:
        return "Wear t-shirt and sunglasses"
    elif "Rainy" in weather:
        return "Take jacket and umbrella"
    return "Wear normal clothes"

# Tool executer
def execute_tool_call(tool_call):
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    if tool_name == "get_weather":
        return get_weather.invoke(tool_args)
    
    elif tool_name == "suggest_clothes":
        return suggest_clothes.invoke(tool_args)

llm_with_tools = llm.bind_tools([get_weather,suggest_clothes])

messages = [

    HumanMessage(

        content=
        "Check weather in Peshawar "
        "and suggest clothes."
    )
]

response = llm_with_tools.invoke(messages)
messages.append(response)


while response.tool_calls:

    for tool_call in response.tool_calls:
        tool_call_result = execute_tool_call(tool_call)

        messages.append(
            ToolMessage(
                content=str(tool_call_result),
                tool_call_id=tool_call["id"]
            )
        )
    response = llm_with_tools.invoke(messages)
    messages.append(response)

print(f"Final answer: {response.content}")