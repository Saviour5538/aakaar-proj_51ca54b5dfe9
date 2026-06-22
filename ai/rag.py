import os
from typing import List, Dict
from .vector_store import VectorStore
from .embeddings import get_embedding
from openai import OpenAI

def retrieve_context(query: str, top_k: int, session_id: str, user_id: str) -> List[Dict]:
    """
    Retrieve relevant context for a query by searching the vector store.
    """
    # Lazy initialization of the vector store
    vector_store = VectorStore()

    # Embed the query
    query_embedding = get_embedding([query])[0]

    # Search the vector store
    filters = {"session_id": session_id, "user_id": user_id}
    matches = vector_store.search(query_embedding, top_k, **filters)

    return matches

def answer_question(query: str, session_id: str, user_id: str) -> Dict[str, object]:
    """
    Answer a question by retrieving context and generating a response using the LLM.
    """
    # Retrieve context
    matches = retrieve_context(query, top_k=5, session_id=session_id, user_id=user_id)

    # Extract chunk texts from matches
    context = "\n".join([match["metadata"]["chunk_text"] for match in matches])

    # Build the prompt
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"

    # Lazy initialization of the OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    client = OpenAI(api_key=api_key)

    # Call the LLM
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}]
    )

    # Extract the answer
    answer = response.choices[0].message.content

    # Extract sources
    sources = [match["metadata"]["source"] for match in matches]

    return {"answer": answer, "sources": sources}