from sentence_transformers import SentenceTransformer
import fitz


class RAGEngine:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.docs = self.load_docs("data/mumbai_dcpr.pdf")

    def load_docs(self, path):
        doc = fitz.open(path)
        chunks = []

        for i, page in enumerate(doc):
            text = page.get_text()

            for para in text.split("\n\n"):
                if len(para.strip()) > 100:
                    chunks.append({
                        "text": para.strip(),
                        "page": i + 1
                    })

        return chunks

    def search(self, query, top_k=3):
        query_emb = self.model.encode([query])[0]

        scored = []

        for
