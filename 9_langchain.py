from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from pydantic import BaseModel, Field
from typing import Literal

import os


# =========================================
# STEP 1 — OUTPUT STRUCTURE
# =========================================

class EmailThreat(BaseModel):

    attack_type: str = Field(
        ...,
        description="Type of email attack"
    )

    severity: Literal[
        "low",
        "medium",
        "high",
        "critical"
    ]

    phishing_detected: bool

    recommended_action: str = Field(
        ...,
        max_length=120
    )


# =========================================
# STEP 2 — LLM
# =========================================

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)


# =========================================
# STEP 3 — JSON PARSER
# =========================================

parser = JsonOutputParser(
    pydantic_object=EmailThreat
)


# =========================================
# STEP 4 — PROMPT
# =========================================

prompt = ChatPromptTemplate.from_messages([

    (
        "system",

        """
        You are a SOC email security analyst.

        Analyze suspicious emails carefully.

        {format_instructions}
        """
    ),

    (
        "user",

        """
        Analyze this email:

        {email}
        """
    )
])


# inject parser instructions automatically
prompt = prompt.partial(
    format_instructions=
    parser.get_format_instructions()
)


# =========================================
# STEP 5 — CHAIN
# =========================================

chain = prompt | llm | parser


# =========================================
# STEP 6 — TEST EMAIL
# =========================================

email_text = """
URGENT!

Your Microsoft account has been locked.

Click here immediately to verify your password:
http://microsoft-security-login.xyz

Failure to verify within 10 minutes
will permanently disable your account.
"""


# =========================================
# STEP 7 — RUN CHAIN
# =========================================

result = chain.invoke({

    "email": email_text
})


# =========================================
# STEP 8 — FINAL VALIDATION
# =========================================

validated = EmailThreat(**result)


# =========================================
# STEP 9 — OUTPUT
# =========================================

print("\n=== VALIDATED OBJECT ===\n")

print(validated)

print("\n=== FIELDS ===\n")

print(f"Attack Type: {validated.attack_type}")

print(f"Severity: {validated.severity}")

print(
    f"Phishing Detected: "
    f"{validated.phishing_detected}"
)

print(
    f"Recommended Action: "
    f"{validated.recommended_action}"
)


# raw dict
print("\n=== RAW DICT ===\n")

print(result)

print(type(result))