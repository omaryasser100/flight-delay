import os
from pathlib import Path


from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import multiprocessing

# Function to load everything and return answer for a query
def get_flight_delay_answer(query: str):
        # Get base path where this file lives
    base_path = Path(__file__).resolve().parent.parent  # Go from backend/ → streamlit_front/
    
    # Build correct file path relative to project root
    summary_path = base_path / "data" / "data_explanation_section.txt"
    model_path = base_path / "models" / "tinyllama-1.1b-chat-q4_K_M.gguf"

    # Load knowledge base
    loader = TextLoader(str(summary_path), encoding="utf-8")
    documents = loader.load()

    

    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    # Embedding model
    embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Create or load vectorstore
    vectorstore = FAISS.from_documents(docs, embedding_model)

    # Setup retriever (improved k)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # Load LLM
    llm = LlamaCpp(
        model_path=str(model_path),
        n_ctx=1024,
        max_tokens=128,
        temperature=0.6,
        top_p=0.9,
        n_batch=512,
        n_threads=multiprocessing.cpu_count(),
        stop=["\n\n", "Question:"],
        verbose=False
    )

    # Prompt template
    custom_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""You are a helpful assistant for analyzing flight delay data.
Always answer only using the provided context. Do not generate information not supported by it.
Keep answers factual and concise.

Context:
{context}

Question:
{question}

Answer:
"""
    )

    # Setup QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True,
        chain_type_kwargs={"prompt": custom_prompt}
    )

    # Run the query
    result = qa_chain({"query": query})
    return result["result"]
