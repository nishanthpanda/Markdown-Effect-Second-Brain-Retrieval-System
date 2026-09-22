import os
from typing import List
from google import genai
from chromadb import Documents, EmbeddingFunction, Embeddings

class GeminiEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model_name: str = "text-embedding-004"):
        self.client = genai.Client() # Assumes GEMINI_API_KEY is in environment
        self.model_name = model_name

    def __call__(self, input: Documents) -> Embeddings:
        response = self.client.models.embed_content(
            model=self.model_name,
            contents=input
        )
        return [e.values for e in response.embeddings]
