import os
from dotenv import load_dotenv

# Correct imports
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
# Import the DirectoryLoader
from langchain_community.document_loaders import DirectoryLoader

load_dotenv()

# --- Configuration ---
SOURCE_DIRECTORY = "clinic_docs"
PERSIST_DIRECTORY = "db"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

# --- Loading Documents ---
print(f"Loading documents from {SOURCE_DIRECTORY}...")
# Use DirectoryLoader to load all files from the folder
loader = DirectoryLoader(SOURCE_DIRECTORY, glob="**/*.*", show_progress=True, use_multithreading=True)
documents = loader.load()

# --- Splitting Text ---
print("Splitting documents into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
texts = text_splitter.split_documents(documents)

# --- Embedding and Storing ---
print("Creating embeddings and storing in Chroma DB...")
embedding = OpenAIEmbeddings()
# Create the vector store from the split texts
db = Chroma.from_documents(texts, embedding, persist_directory=PERSIST_DIRECTORY)

print("-" * 50)
print(f"✅ Ingestion complete.")
print(f"Processed {len(documents)} documents into {len(texts)} chunks.")
print(f"Database saved to '{PERSIST_DIRECTORY}'.")


