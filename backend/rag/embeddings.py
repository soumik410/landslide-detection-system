"""
Local embedding generation using sentence-transformers -- no API cost, runs on CPU,
good enough quality for retrieving short geology/historical context passages.
"""
from functools import lru_cache
from config.settings import settings


@lru_cache(maxsize=1)
def _get_model():
    from sentence_transformers import SentenceTransformer  # imported lazily so app startup isn't blocked
    return SentenceTransformer(settings.EMBEDDING_MODEL)


def embed_text(text: str):
    model = _get_model()
    return model.encode(text, normalize_embeddings=True).tolist()


def embed_batch(texts: list):
    model = _get_model()
    return model.encode(texts, normalize_embeddings=True).tolist()