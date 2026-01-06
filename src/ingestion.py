import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
# 1. NEW IMPORT (Faster)
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import config

def get_loader(file_path: str, file_ext: str):
    if file_ext == ".pdf":
        return PyPDFLoader(file_path)
    elif file_ext == ".docx":
        return Docx2txtLoader(file_path)
    elif file_ext in [".txt", ".md"]:
        return TextLoader(file_path)
    return None

def ingest_documents(uploaded_files):
    if not uploaded_files:
        return "No files provided."

    all_docs = []
    
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[1]
        temp_name = f"temp_{file.name}"
        
        with open(temp_name, "wb") as f:
            f.write(file.getbuffer())
            
        loader = get_loader(temp_name, file_ext)
        if loader:
            all_docs.extend(loader.load())
            
        if os.path.exists(temp_name):
            os.remove(temp_name)

    if not all_docs:
        return "No valid text found in files."

    # 2. OPTIMIZED CHUNKING (Larger chunks = Less processing)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000, 
        chunk_overlap=100
    )
    chunks = splitter.split_documents(all_docs)

    # 3. FAST EMBEDDINGS (The Speed Hack)
    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(config.VECTOR_DB_PATH)
    
    return "Success"