from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, Task, Crew,LLM
import os

llm = LLM(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

# ===================================
# AGENTS — har agent ka role hota hai
# ===================================

log_analyzer = Agent(
    role="SOC Log Analyzer",
    goal="Analyze security logs and identify threats",
    backstory="Expert SOC analyst with 10 years experience in threat detection",
    llm=llm,
    verbose=True
)

threat_hunter = Agent(
    role="Threat Hunter",
    goal="Investigate threats and provide actionable recommendations",
    backstory="Senior threat hunter specializing in incident response",
    llm=llm,
    verbose=True
)

# ===================================
# TASKS — har agent kya karega
# ===================================

analyze_task = Task(
    description="""Analyze this security log and identify:
    1. Threat type
    2. Severity (low/medium/high/critical)
    3. Brief analysis
    
    Log: SSH brute force from 45.33.32.156 — 500 attempts in 1 minute""",
    expected_output="Threat type, severity level, and 2-line analysis",
    agent=log_analyzer
)

hunt_task = Task(
    description="""Based on the log analysis, provide:
    1. Specific recommendation
    2. Immediate action to take""",
    expected_output="One specific action and recommendation",
    agent=threat_hunter
)

# ===================================
# CREW — agents ko saath kaam karwao
# ===================================

crew = Crew(
    agents=[log_analyzer, threat_hunter],
    tasks=[analyze_task, hunt_task],
    verbose=True
)

# Run
print("="*50)
print("CrewAI SOC Analysis")
print("="*50)

result = crew.kickoff()
print("\n=== FINAL RESULT ===")
print(result)