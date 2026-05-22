from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import tempfile
import os

# Page config
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 RAG Chatbot")
st.caption("Upload a PDF and ask questions!")

# Session state — memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chain" not in st.session_state:
    st.session_state.chain = None

# PDF Upload
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    with st.spinner("Processing PDF..."):
        # Temp file banao
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
            f.write(uploaded_file.read())
            tmp_path = f.name

        # Load + chunk
        loader = PyPDFLoader(tmp_path)
        pages = loader.load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(pages)

        # Embeddings + vectorstore
        embeddings = OpenAIEmbeddings(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        vectorstore = FAISS.from_documents(chunks, embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

        # Chain
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY")
        )
        prompt = ChatPromptTemplate.from_template("""
        You are a helpful assistant. Use the context below to answer the question.
        Extract relevant information from the context and provide a clear answer.
        If the context has related information, use it even if not exact.
        Only say "I don't know" if there is truly NO related information.

        Context: {context}

        Question: {question}

        Answer:
        """)

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        # Debug — dekho kya retrieve ho raha hai
        test_docs = retriever.invoke("What is LangGraph?")
        st.write("DEBUG - Retrieved chunks:")
        for i, doc in enumerate(test_docs):
         st.write(f"Chunk {i+1}: {doc.page_content[:200]}")

        st.session_state.chain = (
            {
                "context": retriever | format_docs,
                "question": lambda x: x
            }
            | prompt
            | llm
            | StrOutputParser()
        )

        st.success(f"✅ PDF processed! {len(chunks)} chunks ready.")

# Chat history display
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if question := st.chat_input("Ask something about your PDF..."):
    if st.session_state.chain is None:
        st.warning("Please upload a PDF first!")
    else:
        # User message
        st.session_state.chat_history.append({
            "role": "user",
            "content": question
        })
        with st.chat_message("user"):
            st.write(question)

        # AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = st.session_state.chain.invoke(question)
                st.write(answer)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer
                })