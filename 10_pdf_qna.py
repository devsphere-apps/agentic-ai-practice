from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from typing import Literal
from pydantic import BaseModel,Field

import os



loader = PyPDFLoader("sample.pdf")

docs = loader.load()

pdf_text = ""

for doc in docs:
    pdf_text +=doc.page_content

    # LLM 

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

# prompt builder

prompt = ChatPromptTemplate.from_messages([
    (
        "system",

        """
        You are a helpful PDF assistant.

        Answer in this tone:
        {tone}

        Answer in this language:
        {language}

        Keep Answer Length:
        {answer_size}

        Answer ONLY from the provided PDF context.

        If answer does not exist in PDF,
        say:
        "I could not find this in the PDF."

        PDF Context:
        {context}
        """
    ),
    (
        "user",

        "{question}"
    )
])

parser = StrOutputParser()

chain = prompt | llm | parser

result = chain.invoke({
    "context": pdf_text,
    "question":
    "What does the PDF say about vulputate?",
    "tone":"angry",
    "language":"Roman Urdu",
    "answer_size":"2 lines"
})


print("\n=== PDF ANSWER ===\n")
print(result)