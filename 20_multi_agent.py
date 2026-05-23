from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from typing import Literal
import os

llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

class SOCState(BaseModel):

    log: str
    threat_type: str = ""
    severity: str = ""
    analysis: str = ""
    recommendation: str = ""
    alert_created: bool = False
    final_report: str = ""

# Agent 1: log analyzer 

def log_analyzer_agent(state: SOCState) -> dict:
    response = llm.invoke(f"""
    You are a SOC log analyzer. Analyze this log and identify:
    1. Threat type (one phrase)
    2. Severity (low/medium/high/critical)
    3. Brief analysis (2 lines)

    Log: {state.log}

    Reply in this exact format:
    THREAT: <threat type>
    SEVERITY: <severity>
    ANALYSIS: <analysis>
    """)
    text = response.content
    threat = text.split("THREAT:")[1].split("\n")[0].strip()
    severity = text.split("SEVERITY:")[1].split("\n")[0].strip().lower()
    analysis = text.split("ANALYSIS:")[1].strip()
    return {"threat_type": threat, "severity": severity, "analysis": analysis}

# ===================================
# AGENT 2: Threat Hunter
# ===================================
def threat_hunter_agent(state: SOCState) -> dict:
    print("\n🎯 Threat Hunter Agent running...")
    response = llm.invoke(f"""
You are a threat hunter. Based on this threat analysis, provide specific recommendation.

Threat: {state.threat_type}
Severity: {state.severity}
Analysis: {state.analysis}

Provide ONE specific action to take. Be direct and concise.
""")
    return {"recommendation": response.content.strip()}

# ===================================
# AGENT 3: Alert Creator
# ===================================
def alert_creator_agent(state: SOCState) -> dict:
    print("\n🚨 Alert Creator Agent running...")
    report = f"""
=== SOC ALERT REPORT ===
Log: {state.log}
Threat: {state.threat_type}
Severity: {state.severity.upper()}
Analysis: {state.analysis}
Recommendation: {state.recommendation}
Status: ALERT CREATED ✅
=======================
"""
    return {"alert_created": True, "final_report": report}

# ===================================
# AGENT 4: Skip Alert (low severity)
# ===================================
def skip_alert_agent(state: SOCState) -> dict:
    print("\n✅ Low severity — logging only")
    return {
        "alert_created": False,
        "final_report": f"LOW SEVERITY LOG — Logged only\nThreat: {state.threat_type}"
    }


# ===================================
# ROUTER
# ===================================
def route_severity(state: SOCState) -> Literal["alert_creator", "skip_alert"]:
    if state.severity in ["high", "critical"]:
        return "alert_creator"
    return "skip_alert"

# ===================================
# GRAPH
# ===================================
graph = StateGraph(SOCState)

graph.add_node("log_analyzer", log_analyzer_agent)
graph.add_node("threat_hunter", threat_hunter_agent)
graph.add_node("alert_creator", alert_creator_agent)
graph.add_node("skip_alert", skip_alert_agent)

graph.set_entry_point("log_analyzer")
graph.add_edge("log_analyzer", "threat_hunter")
graph.add_conditional_edges("threat_hunter", route_severity)
graph.add_edge("alert_creator", END)
graph.add_edge("skip_alert", END)

app = graph.compile()

# ===================================
# TEST
# ===================================
if __name__ == "__main__":
    # High severity test
    print("="*50)
    print("TEST 1: High Severity Log")
    print("="*50)
    result = app.invoke(SOCState(
        log="SSH brute force from 45.33.32.156 — 500 attempts in 1 minute"
    ))
    print(result['final_report'])

    # Low severity test
    print("\n" + "="*50)
    print("TEST 2: Low Severity Log")
    print("="*50)
    result2 = app.invoke(SOCState(
        log="User logged in successfully from 192.168.1.1"
    ))
    print(result2['final_report'])
