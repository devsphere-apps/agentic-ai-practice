from dotenv import load_dotenv
load_dotenv()

import asyncio
import os
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient

# LLM client
client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

# Agent 1: Log Analyzer
log_analyzer = AssistantAgent(
    name="LogAnalyzer",
    model_client=client,
    system_message="""You are a SOC Log Analyzer.
    Analyze security logs and identify:
    - Threat type
    - Severity (low/medium/high/critical)
    - Brief analysis
    After analysis, say ANALYSIS_DONE"""
)

# Agent 2: Threat Hunter
threat_hunter = AssistantAgent(
    name="ThreatHunter",
    model_client=client,
    system_message="""You are a Threat Hunter.
    Based on the log analysis provided:
    - Give specific recommendation
    - Give immediate action
    After recommendation, say REPORT_COMPLETE"""
)

# Termination condition
termination = TextMentionTermination("REPORT_COMPLETE")

# Team — agents milke kaam karte hain
team = RoundRobinGroupChat(
    participants=[log_analyzer, threat_hunter],
    termination_condition=termination
)

# Run
async def main():
    print("="*50)
    print("AutoGen SOC Analysis")
    print("="*50)

    log = "SSH brute force from 45.33.32.156 — 500 attempts in 1 minute"

    async for message in team.run_stream(task=log):
        if hasattr(message, 'source') and hasattr(message, 'content'):
            print(f"\n🤖 {message.source}:")
            print(message.content)

asyncio.run(main())