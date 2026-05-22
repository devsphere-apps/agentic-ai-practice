from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
import os

llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

@tool
def check_ip_reputation(ip_address: str) -> str:
    """Check if an IP Address is malicious or safe."""
    malicious_ips = ["10.0.0.5", "192.168.1.105", "45.33.32.156"]
    if ip_address in malicious_ips:
        return f"MALICIOUS: {ip_address} is a known threat actor IP"
    return f"SAFE: {ip_address} has no threat history"

@tool
def create_alert(severity: str, message: str) -> str:
    """Create a security alert in the system"""
    return f"ALERT CREATED — Severity: {severity.upper()} | Message: {message}"

def execute_tool_call(tool_call):
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]
    print(f"\nTool Name: {tool_name}")
    print(f"Tool Args: {tool_args}")
    if tool_name == "check_ip_reputation":
        return check_ip_reputation.invoke(tool_args)
    elif tool_name == "create_alert":
        return create_alert.invoke(tool_args)

llm_with_tools = llm.bind_tools([check_ip_reputation, create_alert])

# Messages history
messages = [HumanMessage("Check IP 10.0.0.5 and if malicious create a high alert")]

# Pehla call
response = llm_with_tools.invoke(messages)
messages.append(response)

# Loop — jab tak tool calls hain
while response.tool_calls:
    print(f"\n--- Tool calls: {len(response.tool_calls)} ---")
    
    for tool_call in response.tool_calls:
        tool_result = execute_tool_call(tool_call)
        print(f"Tool Result: {tool_result}")
        
        messages.append(ToolMessage(
            content=str(tool_result),
            tool_call_id=tool_call["id"]
        ))
    
    # LLM ko dobara call karo
    response = llm_with_tools.invoke(messages)
    messages.append(response)

# Final answer
print(f"\nFinal Answer: {response.content}")