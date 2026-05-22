from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


import os

print("Loading PDF")
loader = PyPDFLoader("agentic-ai.pdf")
pages = loader.load()

print(f"Total Pages: {len(pages)}")

# Cut big PDF into small pieces, So LLM can not read the entier huge pdf, so we need small readable chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # each chunks has 500 characters
    chunk_overlap=50 
    # make sure the start of each next chuck will be the end of the frist chunck, 
    # eg. 
    # chunck_1: Aquick Brown Fox Jump, 
    # chunk_2: Fox Jump over the lazy Dog.
)

chunks = splitter.split_documents(pages)

print(f"Total Chunks: {len(chunks)}")

print("\n Creating embeddings...")


# Convert Chunks Meanings into Vectors(numbers) 
# Eg. "LangGraph is workflow framework" == "[0.22, -0.81, 0.55 ...]"
# This is called semantic meaning
embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

# Store All Vectors in AI memory DB , FAISS does semantic search(will return if meaning are closed to each other not keyword search like)
vectorstore = FAISS.from_documents(chunks,embeddings)
print("Vector store ready")

# Search Engine will retrive the top 3 closed relevent chunks from the vector db
retriever = vectorstore.as_retriever(
    search_kwargs={"k":3}
)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

prompt = ChatPromptTemplate.from_template(
    """
     Answer the question based ONLY on the context below.
     If answer is not in context, say "I don't know".

     Context: {context}

     Question: {question}
    """
)

# combine retrieved chunks into ONE context
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


chain = (
    {
        "context": retriever | format_docs,
        "question": lambda x: x
    }
    | prompt
    | llm
    | StrOutputParser()
)

print("\n" + "="*40)
questions = [
    "What is Agentic AI?",
    "What is LangGraph used for?",
    "What is RAG?"
]

for q in questions:
    print(f"\n❓ {q}")
    answer = chain.invoke(q)
    print(f"💬 {answer}")


#===============
# Mental Modal Simplest format to understand the whole code (RAG)
# What is RAG
# First it will got embedded (convert into vector format)
# FAISS search for which chunks have closest meaning?
# Retriever return top 3 relevent chunks
# Format docs combine retrieved chunks into one context
# Chunks added to prompt 
# LLM answer
#===============