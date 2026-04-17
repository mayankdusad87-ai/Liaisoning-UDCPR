from sentence_transformers import SentenceTransformer
import chromadb


class RAGEngine:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection("dcpr")

    def search(self, query, top_k=3):
        query_embedding = self.model.encode([query]).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )

        docs = []

        for doc, meta in zip(
            results["documents"][0],
            results["metadatas"][0]
        ):
            docs.append(f"[Page {meta['page']}]\n{doc}")

        return docs
