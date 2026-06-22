import os
from typing import List
import openai

# Embedding client for OpenAI's text-embedding-3-small model
class EmbeddingClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        self.model = "text-embedding-3-small"

    def embed_text(self, text: str) -> List[float]:
        """
        Generate an embedding for a single text string.
        """
        response = openai.Embedding.create(
            input=text,
            model=self.model,
            api_key=self.api_key
        )
        return response['data'][0]['embedding']

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a batch of text strings.
        """
        response = openai.Embedding.create(
            input=texts,
            model=self.model,
            api_key=self.api_key
        )
        return [item['embedding'] for item in response['data']]

# Module-level function to embed a list of texts
def get_embedding(texts: List[str]) -> List[List[float]]:
    """
    Embed a list of text strings and return their embeddings.
    """
    client = EmbeddingClient()
    return client.embed_batch(texts)