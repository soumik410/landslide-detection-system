import os
from rag.embeddings import embed_batch
from rag.vector_db import vector_store
from config.settings import settings

CHUNK_SIZE = 500  # characters per chunk -- simple fixed-size chunking, fine for short reference docs


def _chunk_text(text: str, chunk_size: int = CHUNK_SIZE) -> list:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks, buf = [], ""
    for p in paragraphs:
        if len(buf) + len(p) > chunk_size and buf:
            chunks.append(buf.strip())
            buf = ""
        buf += p + "\n\n"
    if buf.strip():
        chunks.append(buf.strip())
    return chunks


def ingest_directory(directory: str = None):
    directory = directory or settings.KNOWLEDGE_BASE_DIR
    if not os.path.isdir(directory):
        print(f"No knowledge base directory found at {directory}")
        return 0

    all_chunks, all_meta = [], []
    for fname in os.listdir(directory):
        if not fname.endswith((".txt", ".md")):
            continue
        category = "historical" if "historical" in fname.lower() else "geology"
        with open(os.path.join(directory, fname), "r", encoding="utf-8") as f:
            text = f.read()
        for i, chunk in enumerate(_chunk_text(text)):
            all_chunks.append(chunk)
            all_meta.append({"source": fname, "chunk_id": i, "category": category, "text": chunk})

    if not all_chunks:
        print("No .txt/.md documents found to ingest.")
        return 0

    vectors = embed_batch(all_chunks)
    for vec, meta in zip(vectors, all_meta):
        vector_store.add(vec, meta)
    vector_store.save()
    print(f"Ingested {len(all_chunks)} chunks from {directory}")
    return len(all_chunks)


if __name__ == "__main__":
    ingest_directory()