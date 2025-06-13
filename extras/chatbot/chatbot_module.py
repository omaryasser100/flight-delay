import os
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.llms import HuggingFacePipeline

# ✅ Safe cache for HF Spaces
os.environ["TRANSFORMERS_CACHE"] = "/tmp/hf_cache"
os.environ["HF_HOME"] = "/tmp/hf_home"

# ✅ Require token for HF model access
if not os.environ.get("HUGGINGFACEHUB_API_TOKEN"):
    raise EnvironmentError("❌ HUGGINGFACEHUB_API_TOKEN not found! Set it in your HF Space secrets.")

def load_vectorstore():
    embedder = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        cache_folder="/tmp/hf_cache"
    )
    loader = TextLoader("app/data/analysis_summary.txt")
    docs = loader.load()

    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    store = FAISS.from_documents(chunks, embedder)
    return store.as_retriever()

def build_qa_chain():
    # ✅ Load FLAN-T5 Base
    model_name = "google/flan-t5-base"
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name, cache_dir="/tmp/hf_cache")
    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir="/tmp/hf_cache")

    pipe = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=128
    )

    llm = HuggingFacePipeline(pipeline=pipe)
    retriever = load_vectorstore()

    # ✅ Custom prompt (simple and editable)
    prompt_template = PromptTemplate.from_template(
        "Answer the question based only on the following context:\n\n"
        "{context}\n\n"
        "Question: {question}\nAnswer:"
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt_template}
    )

# ✅ Build QA chain once
qa_chain = build_qa_chain()

def get_bot_answer(query: str) -> str:
    try:
        return qa_chain.run(query)
    except Exception as e:
        return f"❌ Error: {str(e)}"
