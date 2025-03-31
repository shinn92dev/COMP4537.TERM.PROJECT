from langchain_ollama import OllamaLLM
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import FastEmbedEmbeddings
import os
import requests
import json

try:
    requests.get("http://localhost:11434", timeout=3)
except requests.exceptions.ConnectionError:
    print("❌ Ollama Server is not on.")
    raise

llm = OllamaLLM(model="llama3.2")

loader = DirectoryLoader("./utils/store", glob="*.txt", loader_cls=lambda path: TextLoader(path, encoding="utf-8"))
documents = loader.load()

if not documents:
    print("⚠️ No documents found. Proceeding with empty context.")

splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000, chunk_overlap=200)
docs = splitter.split_documents(documents) if documents else []

retriever = None
if docs:
    embeddings = FastEmbedEmbeddings()
    vStore = Chroma.from_documents(docs, embedding=embeddings, persist_directory="vectorStore")
    retriever = vStore.as_retriever()
    print(f"📁 {len(docs)} documents loaded into vector store.")
else:
    print("⚠️ No documents found. Proceeding with fallback LLM-only method.")
vector_store_path = "vectorStore"
vStore = Chroma.from_documents(docs, embedding=embeddings, persist_directory=vector_store_path)
retriever = vStore.as_retriever()

prompt = PromptTemplate.from_template("""
You are a smart lighting assistant. Based on the input, suggest a HEX color for a smart lamp, the reason for choosing it, and one piece of helpful advice.

If you have no context, guess based on common mood-lighting knowledge.

INPUT:
{input}

Context:
{context}

Respond in JSON like this:
{{"color": "#FF5733", "reason": "Orange energizes you", "advice": "Open the window for fresh air"}}
""")

rag_chain = None
if retriever:
    doc_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, doc_chain)

def ask_to_ai_rag(prompt_input: str) -> dict:
    try:
        if rag_chain:
            response = rag_chain.invoke({"input": prompt_input})
            return json.loads(response["answer"])
        else:
            formatted = prompt.format(input=prompt_input, context="")
            result = llm.invoke(formatted)
            return json.loads(result)
    except Exception as e:
        print("❌ Error in ask_to_ai_rag:", e)
        raise
