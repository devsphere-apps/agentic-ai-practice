from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI 
from langgraph.graph import StateGraph,START,END
from typing import Literal, TypedDict
import json
import os


llm = ChatOpenAI(model="gpt-4o-mini",api_key=os.getenv("OPENAI_API_KEY"))

class EmailClassification(TypedDict):
    intent:Literal["spam","question",'complaint','praise','request']
    urgency:Literal["low","medium","high","critical"]
    topic:str
    summary:str

# main state
class EmailAgentState(TypedDict):
    email_subject:str
    email_content:str
    email_sender:str
    email_id:str
    classification:EmailClassification | None
    search_results:list[str] | None
    draft_response:str | None

# Email Classification Node
def classify_email(state:EmailAgentState)->dict:
    """Node 1 : Classifiy the email based on provided state"""

    response= llm.invoke([
        SystemMessage(
            content="""You are an email classifier.
            Analyze the email and return ONLY valid JSON:
            {
                "intent": "spam|question|complaint|praise|request",
                "urgency": "low|medium|high|critical",
                "topic": "short topic",
                "summary": "one line summary"
            }  
            """
        ),
        HumanMessage(
            content=f"""
            Subject:{state["email_subject"]}
            Content:{state["email_content"]}
            Sender:{state["email_sender"]}
            """
        )
    ])

    classification = json.loads(response.content)
    return {"classification": classification}

# Draft reply creator node

def draft_reply(state:EmailAgentState)->dict:
    """Node 2 : Draft a reply based on the email classification and content"""
    classification = state["classification"]

    response = llm.invoke([
        SystemMessage(
            content="""You are a professional customer support agent.
            Write a helpful, polite email reply.
Keep it concise — max 3 paragraphs."""
        ),
        HumanMessage(
            content=f"""
            Original Email:
            Subject: {state['email_subject']}
            From: {state['email_sender']}
            Content: {state['email_content']}

            Classification:
            Intent: {classification['intent']}
            Urgency: {classification['urgency']}
            Topic: {classification['topic']}
            Summary: {classification['summary']}

            Write a professional reply.
           """
        )
    ])
    return {"draft_response": response.content}

def route_email(state:EmailAgentState)->Literal["draf_reply","__end__"]:
    """Router Node: Decide whether to draft a reply or end it based on email intent is spam"""
     
    if state["classification"]["intent"] == "spam":
        return "__end__"
    else:
        return "draft_reply"



# Create a graph
graph = StateGraph(EmailAgentState)

# Add nodes to the graph

graph.add_node("classify_email", classify_email)
graph.add_node("draft_reply", draft_reply)

# add edges
graph.add_edge(START,"classify_email")
graph.add_conditional_edges("classify_email",route_email,["draft_reply","__end__"])
graph.add_edge("draft_reply", END)

agent = graph.compile()

# Test — 2 emails
emails = [
    {
        "subject": "Question about product",
        "content": "I have a question about your product features.",
        "sender": "customer@gmail.com",
        "id": "001"
    },
    {
        "subject": "WIN FREE IPHONE!!!",
        "content": "Click here to claim your prize now!!!",
        "sender": "spam@spam.com",
        "id": "002"
    }
]

for email in emails:
    print(f"\n{'='*40}")
    result = agent.invoke(EmailAgentState(
        email_subject=email["subject"],
        email_content=email["content"],
        email_sender=email["sender"],
        email_id=email["id"],
        classification=None,
        search_results=None,
        draft_response=None
    ))
    print(f"Intent: {result['classification']['intent']}")
    print(f"Draft: {result['draft_response'] or 'No reply — spam!'}")    