import chromadb
from sentence_transformers import SentenceTransformer


class RAGEngine:

    def __init__(self):
        self.embedder = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.client = chromadb.PersistentClient(
            path="./vector_db"
        )

        self.collection = self.client.get_collection(
            "udcpr"
        )

    def search(self, query, top_k=3):
        embedding = self.embedder.encode(
            [query]
        ).tolist()

        result = self.collection.query(
            query_embeddings=embedding,
            n_results=top_k
        )

        return result["documents"][0]
