"""
Minimal in-process vector store (numpy cosine similarity + pickle persistence).
Avoids pulling in a full vector-database dependency for a project this size --
swap this module out for Chroma/FAISS/pgvector later without touching retriever.py,
since callers only ever use add() / search() / save() / load().
"""
import pickle
import os
import numpy as np
from config.settings import settings


class VectorStore:
    def __init__(self, path: str = None):
        self.path = path or settings.VECTOR_DB_PATH
        self.vectors = []   # list[list[float]]
        self.metadata = []  # list[dict] (source, chunk text, etc.), same index as vectors
        self._load()

    def add(self, vector: list, meta: dict):
        self.vectors.append(vector)
        self.metadata.append(meta)

    def search(self, query_vector: list, top_k: int = 3) -> list:
        if not self.vectors:
            return []
        mat = np.array(self.vectors)
        q = np.array(query_vector)
        scores = mat @ q  # vectors are pre-normalized, so dot product == cosine similarity
        top_idx = np.argsort(-scores)[:top_k]
        return [{"score": float(scores[i]), **self.metadata[i]} for i in top_idx]

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "wb") as f:
            pickle.dump({"vectors": self.vectors, "metadata": self.metadata}, f)

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, "rb") as f:
                data = pickle.load(f)
                self.vectors = data.get("vectors", [])
                self.metadata = data.get("metadata", [])


vector_store = VectorStore()