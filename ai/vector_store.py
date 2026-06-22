import os
import psycopg2
from psycopg2.extras import Json
from typing import List, Dict

class VectorStore:
    def __init__(self):
        self.connection_string = os.getenv("PGVECTOR_CONNECTION_STRING")
        if not self.connection_string:
            raise ValueError("PGVECTOR_CONNECTION_STRING environment variable is not set.")
        self.table_name = "vector_store"

    def _connect(self):
        """
        Establish a connection to the PostgreSQL database.
        """
        return psycopg2.connect(self.connection_string)

    def upsert(self, id: str, vector: List[float], metadata: Dict):
        """
        Upsert a vector and its metadata into the vector store.
        """
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    INSERT INTO {self.table_name} (id, vector, metadata)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (id) DO UPDATE
                    SET vector = EXCLUDED.vector,
                        metadata = EXCLUDED.metadata;
                """, (id, vector, Json(metadata)))
                conn.commit()

    def search(self, query_embedding: List[float], top_k: int, **filters) -> List[Dict]:
        """
        Search for the top_k closest vectors to the query_embedding.
        """
        filter_conditions = " AND ".join(
            [f"metadata->>'{key}' = %s" for key in filters.keys()]
        )
        filter_values = list(filters.values())

        query = f"""
            SELECT id, metadata, 1 - (vector <=> %s) AS distance
            FROM {self.table_name}
            {"WHERE " + filter_conditions if filters else ""}
            ORDER BY vector <=> %s
            LIMIT %s;
        """

        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, [query_embedding] + filter_values + [query_embedding, top_k])
                results = cur.fetchall()

        return [
            {"id": row[0], "metadata": row[1], "distance": row[2]}
            for row in results
        ]