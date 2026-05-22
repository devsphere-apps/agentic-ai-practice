from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Literal
import json
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

class LogSummary(BaseModel):
    
    log_type:Literal["auth", "network", "system"]

    risk_score:int = Field(
        ...,
        ge=1,
        le=10,
        description="Risk power of the attack"
    )
    recommended_action:str
    need_escalation:bool

def analyze_log(log_input:str)->LogSummary:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role":"system",
                "content":""" You are a SOC analyst. 
                Analyze the log entry and respond ONLY in this JSON format:
                {
                    "log_type": "auth|network|system",
                    "risk_score": "int (1-10)",
                    "recommended_action": "str",
                    "need_escalation": true|false
                } """
            },
            {
                "role":"user",
                "content":f"Analyze this {log_input}"
            }
        ]
    )

    raw = response.choices[0].message.content
    print(f"Raw data {raw}")
    print()
    data = json.loads(raw)
    return LogSummary(**data)

if __name__=="__main__":

    log = "Outbound connection to known malware C2 server 45.33.32.156 on port 443"
    
    result = analyze_log(log)

    print(f"Validated result")
    print(f"\nLog Type: {result.log_type}")
    print(f"Risk Score: {result.risk_score}")
    print(f"Recommended Action: {result.recommended_action}")
    print(f"Needs Escalation: {result.need_escalation}")