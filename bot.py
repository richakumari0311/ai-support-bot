from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import ollama
from dotenv import load_dotenv
import os

load_dotenv()

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import ollama

# Load & chunk the FAQ file
def load_knowledge_base(filepath="knowledge_base/faqs.txt"):
    """Load and split the FAQ file into chunks"""

    loader = TextLoader(filepath)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", "Q:"]
    )
    chunks = splitter.split_documents(documents)
    print(f"Loaded {len(chunks)} knowledge chunks from {filepath}")
    return chunks

# Build the vector database
def build_vector_store(chunks, persist_dir="chroma_db"):
    print("Building vector store (first run takes around 30 secs).....")

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )

    print("Vector store ready!")
    return vector_store

# Load existing vector store (skip rebuidling every time)
def load_vector_store(persist_dir="chroma_db"):
    embeddings= HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vector_store = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )
    print("Vector store loaded from disk")
    return vector_store

# Search for relevent FAQ chunks
def search_knowledge_base(vector_store, question, k=3):
    results = vector_store.similarity_search(question, k=k)
    context = "\n\n".join([doc.page_content for doc in results])
    return context

# Ask the bot with rag context
def ask_bot(vector_store, user_question):
    # Find relevant FAQ chunks
    context = search_knowledge_base(vector_store, user_question)

    # Build prompt with context injected
    prompt = f"""You are a helpful customer support assiatant.
    Use ONLY the information below to answer the questions.
    If the answer is not in the information below, say:
    "I don't have that information, Please contact support@company.com"

--- KNOWLEDGE BASE ---
{context}
--- END ---

Customer question: {user_question}
Answer:"""
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content":prompt}]
    )
    return response["message"]["content"]

# Build store once and then test
if __name__ == "__main__":
    # Build vectore store if it doesn't exist yet
    if not os.path.exists("chroma_db"):
        chunks = load_knowledge_base()
        vector_store = build_vector_store(chunks)
    else:
        vector_store = load_vector_store()

    # Test questions
    test_questions = [
        "Where is my order?",
        "Can I get my money back?",
        "Do you take PayPal?",
        "What if my package was broken?",
        "How do I earn rewards points?",
    ]   
    print("\n" + "="*55)
    for question in test_questions:
        print(f"\n {question}")
        print(f" {ask_bot(vector_store, question)}")
        print("-" * 55)