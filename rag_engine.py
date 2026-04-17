from sentence_transformers import SentenceTransformer
import fitz
import numpy as np


class RAGEngine:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Load and prepare documents once
        self.docs = self.load_docs("data/mumbai_dcpr.pdf")

        # Precompute embeddings
        self.embeddings = self.model.encode(
            [d["text"] for d in self.docs],
            convert_to_numpy=True
        )

    # -----------------------------------
    # LOAD + CHUNK PDF
    # -----------------------------------
    def load_docs(self, path):
        try:
            doc = fitz.open(path)
        except Exception as e:
            print(f"PDF Load Error: {e}")
            return []

        chunks = []

        for i, page in enumerate(doc):
            text = page.get_text()

            paragraphs = text.split("\n\n")

            for para in paragraphs:
                para = para.strip()

                if len(para) > 120:
                    chunks.append({
                        "text": para,
                        "page": i + 1
                    })

        print(f"Loaded {len(chunks)} chunks from PDF")
        return chunks

    # -----------------------------------
    # COSINE SIMILARITY
    # -----------------------------------
    def cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    # -----------------------------------
    # SEARCH (SEMANTIC)
    # -----------------------------------
    def search(self, query, top_k=3):

        if not self.docs:
            return []

        query_embedding = self.model.encode([query])[0]

        scores = []

        for i, emb in enumerate(self.embeddings):
            sim = self.cosine_similarity(query_embedding, emb)
            scores.append((sim, i))

        # Sort by similarity
        scores.sort(reverse=True, key=lambda x: x[0])

        results = []

        for score, idx in scores[:top_k]:
            chunk = self.docs[idx]

            results.append(
                f"[Page {chunk['page']} | Score: {round(score, 2)}]\n{chunk['text']}"
            )

        return results
