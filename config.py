import os

# Paths
VECTOR_DB_PATH = "vectorstore/db_faiss"

# Model Configurations
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# --- UPDATED MODEL NAMES (2025) ---
# Groq renamed their models. We must use the new identifiers.
LLM_FAST = "llama-3.1-8b-instant"         # Replaces llama3-8b-8192
LLM_SMART = "llama-3.3-70b-versatile"     # Replaces llama3-70b-8192

# Ingestion Settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 500
RETRIEVAL_SEARCH_K = 6