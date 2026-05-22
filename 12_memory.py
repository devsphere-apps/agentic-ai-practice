from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
import os

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

# Memory — simple list of messages
conversation_history = []
MAX_MESSAGES = 6


def chat(user_message: str) -> str:
    # User message add karo history mein
    conversation_history.append(
        HumanMessage(content=user_message)
    )

    # Sirf last MAX_MESSAGES bhejo LLM ko
    recent = conversation_history[-MAX_MESSAGES:]
    # Poori history LLM ko bhejo
    response = llm.invoke(recent)
    
    # AI response bhi save karo
    conversation_history.append(
        AIMessage(content=response.content)
    )
    
    return response.content

# Test — kya agent yaad rakhta hai?
print("Turn 1:", chat("My name is Abdul Mateen, SOC analyst"))
print("Turn 2:", chat("I work in Peshawar"))
print("Turn 3:", chat("What is virus in two line?"))
print("Turn 4:", chat("What is my name and city?"))  # yaad hai?

print(f"\nTotal messages: {len(conversation_history)}")