from rag.embeddings import embed_text
from rag.vector_db import vector_store


def retrieve(query: str, top_k: int = 3, category: str = None) -> list:
    query_vec = embed_text(query)
    results = vector_store.search(query_vec, top_k=top_k * 2 if category else top_k)
    if category:
        results = [r for r in results if r.get("category") == category][:top_k]
    return results


def retrieve_context_text(query: str, top_k: int = 3, category: str = None) -> str:
    """Convenience helper: retrieval results collapsed into one string ready to drop into an LLM prompt."""
    results = retrieve(query, top_k=top_k, category=category)
    if not results:
        return "No relevant reference material found in the knowledge base."
    return "\n\n".join(f"[{r['source']}] {r['text']}" for r in results)