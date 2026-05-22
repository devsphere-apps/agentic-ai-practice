from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

import os

llm = ChatOpenAI(model="gpt-4o-mini",api_key=os.getenv("OPENAI_API_KEY"))

@tool
def say_hello(name:str)->str:
    """Say hello to someone."""
    return f"Hello {name}"

@tool
def say_good_bye(name:str)->str:
    """Say good bye to someone."""
    return f"hello {name} good bye see you next time"

@tool
def say_thanks(name:str)->str:
    """Say thanks to someone"""
    return f"Thankyou {name}"

# pass the tools to llm

llm_with_tools = llm.bind_tools([say_hello,say_good_bye,say_thanks])

# now call the llm with tools

tests = [

    "Say Good Bye to Mateen",

    "Tell Mateen goodbye politely",

    "Say thanks to Mateen",

    "Say hello to Ali"
]


for test in tests:

    # print(f"\nUSER INPUT: {test}")

    response = llm_with_tools.invoke(test)

    # print(response.tool_calls)

    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call['args']

        print("\nEXECUTING TOOL...")
        
        if tool_name == "say_hello":
            result = say_hello.invoke(tool_args)
        elif tool_name == "say_good_bye":
            result = say_good_bye.invoke(tool_args)
        elif tool_name == "say_thanks":
            result = say_thanks.invoke(tool_args)

        print("\nTOOL RESULT:")
        print(result)


