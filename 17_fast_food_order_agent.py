from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import (HumanMessage,ToolMessage)

import os 

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

@tool
def order_food(name:str,food:str)->str:
    """Will help to order food"""
    return f"{food} successfully ordered for {name} 🍕"

@tool
def send_thanks(name:str)->str:
    """Say thanks to someone"""
    return f"Thanks for order {name}!"

def execute_tools(tool_call):
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    if tool_name == "order_food":
        return order_food.invoke(tool_args)
    elif tool_name == "send_thanks":
        return send_thanks.invoke(tool_args)
    
llm_with_tools = llm.bind_tools([order_food,send_thanks])

messages = [
    HumanMessage(
       content =
        "Order pizza for Mateen"
        "and thank him"
    )
]

respone = llm_with_tools.invoke(messages)
messages.append(respone)

while respone.tool_calls:
    for tool_call in respone.tool_calls:
        tool_call_result = execute_tools(tool_call)

        messages.append(
            ToolMessage(
                content=str(tool_call_result),
                tool_call_id=tool_call["id"]
            )
        )
    respone = llm_with_tools.invoke(messages)
    messages.append(respone)

print(f"Final Result: {respone.content}")