import os
from typing import List, Dict
import pandas as pd
from docx import Document
from .vector_store import VectorStore
from .embeddings import get_embedding

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def chunk(document: str) -> List[str]:
    """
    Chunk the document text using an overlapping strategy.
    """
    chunks = []
    start = 0
    while start < len(document):
        end = min(start + CHUNK_SIZE, len(document))
        chunks.append(document[start:end])
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks

def ingest_document(file_path: str, session_id: str, user_id: str) -> Dict[str, int]:
    """
    Ingest a document by reading, chunking, embedding, and storing it in the vector store.
    """
    # Lazy initialization of the vector store
    vector_store = VectorStore()

    # Determine file type and extract text
    if file_path.endswith(".xlsx") or file_path.endswith(".csv"):
        data = pd.read_excel(file_path, engine="openpyxl") if file_path.endswith(".xlsx") else pd.read_csv(file_path)
        text = "\n".join(data.astype(str).apply(lambda x: " ".join(x), axis=1))
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    elif file_path.endswith(".txt") or file_path.endswith(".md"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        raise ValueError("Unsupported file type")

    # Chunk the text
    chunks = chunk(text)

    # Embed and upsert each chunk
    embeddings = get_embedding(chunks)
    for i, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
        metadata = {
            "session_id": session_id,
            "user_id": user_id,
            "source": file_path,
            "chunk_text": chunk_text,
        }
        vector_store.upsert(f"{session_id}_{user_id}_{i}", embedding, metadata)

    return {"chunks": len(chunks)}