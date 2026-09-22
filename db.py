import os
import chromadb
from chromadb.config import Settings
from app.embeddings import GeminiEmbeddingFunction
from typing import Dict, Any, List

# Initialize chroma client
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_data")
client = chromadb.PersistentClient(path=DB_DIR, settings=Settings(allow_reset=True))

def get_collection():
    return client.get_or_create_collection(
        name="second_brain",
        embedding_function=GeminiEmbeddingFunction()
    )

def search_documents(query: str, top_k: int = 5, where: Dict[str, Any] = None):
    collection = get_collection()
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        where=where if where else None,
        include=["documents", "metadatas", "distances"]
    )
    return results
