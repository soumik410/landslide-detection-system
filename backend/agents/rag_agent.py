from agents.llm_client import call_llm
from rag.retriever import retrieve_context_text

SYSTEM_PROMPT = (
    "You are a reference-grounded assistant. Answer the question using ONLY the "
    "provided context. If the context does not contain enough information, say so "
    "plainly rather than guessing. Keep the answer to 2-3 sentences."
)


def run(query: str, category: str = None, top_k: int = 3) -> str:
    context = retrieve_context_text(query, top_k=top_k, category=category)
    prompt = f"Context:\n{context}\n\nQuestion: {query}"
    try:
        return call_llm(SYSTEM_PROMPT, prompt)
    except Exception as e:
        return f"[rag_agent unavailable: {e}]"