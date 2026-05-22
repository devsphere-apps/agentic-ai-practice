from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph,END
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing import Literal

import os


llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

# Define State , graph data
class AlertState(BaseModel):

    log:str
    severity:str = ""
    action:str =""
    status:str = "pending"

# Step 2: prepare nodes, every nodes work mini task

def analyze_node(state:AlertState)->dict:
    response = llm.invoke(f"Analyze this security log and reply with ONLY: severity=high/medium/low and action=block/monitor/ignore\nLog: {state.log}")

    text = response.content.lower()

    severity = "high" if "high" in text else "medium" if "medium" in text else "low"
    action = "block" if "block" in text else "monitor" if "monitor" in text else "ignore"

    return {"severity":severity,"action":action}

def route_by_severity(state:AlertState)->Literal["high_severity","low_severity"]:

    if state.severity == "high":
        return "high_severity"
    return "low_severity"

def high_severity_node(state:AlertState)->dict:
    return {"status":"escalated"}

def low_severity_node(state:AlertState)->dict:
    return{"status":"logged"}


# Create graph

graph = StateGraph(AlertState)

# Add nodes to the graph

graph.add_node("analyze",analyze_node)
graph.add_node("high_severity",high_severity_node)
graph.add_node("low_severity",low_severity_node)

# Add edges

graph.set_entry_point("analyze")
graph.add_conditional_edges("analyze",route_by_severity)
graph.add_edge("high_severity",END)
graph.add_edge("low_severity",END)

#compile 
app = graph.compile()



# Run 
result = app.invoke(AlertState(
    log="SSH brute force from 10.0.0.5 - 500 attempts in 1 minute"
))

print(f"\nFinal State:")
print(f"Severity: {result['severity']}")
print(f"Action: {result['action']}")
print(f"Status: {result['status']}")

# Low severity test
result2 = app.invoke(AlertState(
    log="User logged in successfully from 192.168.1.1"
))

print(f"\n--- Low Severity Test ---")
print(f"Severity: {result2['severity']}")
print(f"Action: {result2['action']}")
print(f"Status: {result2['status']}")