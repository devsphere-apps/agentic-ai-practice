from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing import Literal
import os

llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

# State
class SOCState(BaseModel):
    log: str
    threat_type: str = ""
    severity: str = ""
    analysis: str = ""
    recommendation: str = ""
    alert_created: bool = False
    final_report: str = ""

# Agents
def log_analyzer_agent(state: SOCState) -> dict:
    response = llm.invoke(f"""
You are a SOC log analyzer. Analyze this log:
Log: {state.log}

Reply in this exact format:
THREAT: <threat type>
SEVERITY: <low/medium/high/critical>
ANALYSIS: <2 line analysis>
""")
    text = response.content
    threat = text.split("THREAT:")[1].split("\n")[0].strip()
    severity = text.split("SEVERITY:")[1].split("\n")[0].strip().lower()
    analysis = text.split("ANALYSIS:")[1].strip()
    return {"threat_type": threat, "severity": severity, "analysis": analysis}

def threat_hunter_agent(state: SOCState) -> dict:
    response = llm.invoke(f"""
You are a threat hunter.
Threat: {state.threat_type}
Severity: {state.severity}
Analysis: {state.analysis}
Provide ONE specific action. Be direct.
""")
    return {"recommendation": response.content.strip()}

def alert_creator_agent(state: SOCState) -> dict:
    report = f"""=== SOC ALERT REPORT ===
Log: {state.log}
Threat: {state.threat_type}
Severity: {state.severity.upper()}
Analysis: {state.analysis}
Recommendation: {state.recommendation}
Status: ALERT CREATED ✅
======================="""
    return {"alert_created": True, "final_report": report}

def skip_alert_agent(state: SOCState) -> dict:
    return {
        "alert_created": False,
        "final_report": f"LOW SEVERITY — Logged only\nThreat: {state.threat_type}"
    }

def route_severity(state: SOCState) -> Literal["alert_creator", "skip_alert"]:
    if state.severity in ["high", "critical"]:
        return "alert_creator"
    return "skip_alert"

# Graph
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
# STREAMLIT UI
# ===================================
st.set_page_config(
    page_title="SOC AI Agent",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ SOC AI Agent")
st.caption("Autonomous Security Log Analyzer — Powered by Multi-Agent AI")

# Example logs
st.subheader("📋 Try these examples:")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔴 Brute Force"):
        st.session_state.log_input = "SSH brute force from 45.33.32.156 — 500 attempts in 1 minute"

with col2:
    if st.button("🟡 Port Scan"):
        st.session_state.log_input = "Port scan detected from 10.0.0.5 — 1000 ports scanned"

with col3:
    if st.button("🟢 Normal Login"):
        st.session_state.log_input = "User admin logged in successfully from 192.168.1.1"

# Input
log_input = st.text_area(
    "Enter Security Log:",
    value=st.session_state.get("log_input", ""),
    height=100,
    placeholder="Paste your security log here..."
)

# Analyze button
if st.button("🔍 Analyze", type="primary"):
    if not log_input:
        st.warning("Please enter a log!")
    else:
        with st.spinner("🤖 Agents analyzing..."):
            result = app.invoke(SOCState(log=log_input))

        # Results
        st.divider()

        # Severity color
        severity = result['severity'].upper()
        color = {
            "CRITICAL": "🔴",
            "HIGH": "🟠",
            "MEDIUM": "🟡",
            "LOW": "🟢"
        }.get(severity, "⚪")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Threat Type", result['threat_type'])
        with col2:
            st.metric("Severity", f"{color} {severity}")
        with col3:
            st.metric("Alert", "✅ Created" if result['alert_created'] else "📝 Logged")

        st.subheader("📊 Analysis")
        st.info(result['analysis'])

        st.subheader("💡 Recommendation")
        st.success(result['recommendation'])

        st.subheader("📄 Full Report")
        st.code(result['final_report'])