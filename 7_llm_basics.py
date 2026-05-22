from openai import OpenAI
import os
from pydantic import BaseModel,Field
from typing import Literal
import json



client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Step 1: Output ka structure define karo
class ThreatAnalysis(BaseModel):
    threat_type: str = Field(..., description="Type of threat")
    severity: Literal["low", "medium", "high", "critical"]
    summary: str = Field(..., max_length=200)
    action_required: bool

# Step 2: LLM se structured output lo
def analyze_threat(log_entry: str) -> ThreatAnalysis:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are a SOC analyst. 
                Analyze the log entry and respond ONLY in this JSON format:
                {
                    "threat_type": "string",
                    "severity": "low|medium|high|critical",
                    "summary": "max 200 chars",
                    "action_required": true|false
                }"""
            },
            {
                "role": "user",
                "content": f"Analyze this log: {log_entry}"
            }
        ]
    )

    # LLM ka raw response
    raw = response.choices[0].message.content
    print(f"Raw LLM output:\n{raw}\n")

    # Pydantic se validate karo
    data = json.loads(raw)
    return ThreatAnalysis(**data)


# Step 3: Test karo
if __name__ == "__main__":
    log = "Failed login attempt from IP 192.168.1.105 - 47 attempts in 2 minutes"
    
    result = analyze_threat(log)
    
    print("Validated Result:")
    print(result)
    print(f"\nSeverity: {result.severity}")
    print(f"Action needed: {result.action_required}")