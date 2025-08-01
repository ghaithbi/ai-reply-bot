import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# Load your OpenAI API key
load_dotenv()

# Load ALL files from the folder
loader = DirectoryLoader(
    "clinic_docs",
    glob="**/*.*",  # Loads all file types recursively
    show_progress=True
)
docs = loader.load()

# Split docs into smaller chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_documents(docs)

# Embed and store in Chroma
embeddings = OpenAIEmbeddings()
vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
vectordb.persist()

print(f"✅ Embedded and stored {len(chunks)} chunks from folder.")


