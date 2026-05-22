from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

import os

llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

@tool
def say_hello(name: str) -> str:
    """Say hello to someone."""

    return f"Hello {name} 😄"


@tool
def say_thanks(name: str) -> str:
    """Say thanks to someone."""

    return f"Thank you {name} 🙌"


@tool
def say_goodbye(name: str) -> str:
    """Say goodbye to someone."""

    return f"Goodbye {name} 👋"


# execute the tools
def execute_tool_call(tool_call):
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    if tool_name == "say_hello":
        return say_hello.invoke(tool_args)
    elif tool_name == "say_thanks":
        return say_thanks.invoke(tool_args)
    elif tool_name == "say_goodbye":
        return say_goodbye.invoke(tool_args)
    
llm_with_tools = llm.bind_tools([say_hello,say_thanks,say_goodbye])

messages = [
    HumanMessage(
        content=
        "Say hello to mateen,"
        "Then thank to him,"
        "Then say goodbye politely"
    )
]

# ===========================
# send conversation history to LLM 
# initiall its contain only user messages
# llm lookup for two things(available tools+user messages)
# then it start reasoning.
# ============================


response = llm_with_tools.invoke(messages)
"""
The return will be tool execution plan
example:
[
   say_hello,
   say_thanks,
   say_goodbye
]
"""


messages.append(response)
"""
Here we were storing AI's tool request
now history look like this
messages = [

   USER:
   "Say hello..."

   AI:
   "I want these tools"
]
"""



"""
while loop -- As long as AI wants tools, keep running loop
"""

while response.tool_calls:
    print(
        f"\n---Tool Calls: "
        f"{len(response.tool_calls)}----"
    )

    # Run EACH requested tool
    for tool_call in response.tool_calls:
        tool_result = execute_tool_call(tool_call)
        print(f"Tool Result: {tool_result}")
        
        # Give tool result BACK to LLM

        messages.append(
            ToolMessage(
                content= str(tool_result),
                tool_call_id= tool_call["id"]
            )
        )
        """
        Now History look like
        messages = [

            USER:
             "Say hello..."

             AI:
              "Use hello tool"

             TOOL:
             "Hello Mateen 😄"
        ]
        """


    # Call LLM again with updated history
    response = llm_with_tools.invoke(messages)

    messages.append(response)

print(f"\n====Final Result=====\n")
print(response.content)