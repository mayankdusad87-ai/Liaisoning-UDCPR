import fitz
from sentence_transformers import SentenceTransformer
import chromadb


class PDFIngestion:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # persistent storage
        self.client = chromadb.PersistentClient(path="./vector_db")
        self.collection = self.client.get_or_create_collection("dcpr")

    def ingest(self, pdf_path):
        doc = fitz.open(pdf_path)

        chunks = []

        for i, page in enumerate(doc):
            text = page.get_text()

            # better chunking
            paragraphs = text.split("\n\n")

            for para in paragraphs:
                para = para.strip()

                if len(para) > 120:
                    chunks.append({
                        "text": para,
                        "page": i + 1
                    })

        print(f"Total chunks: {len(chunks)}")

        texts = [c["text"] for c in chunks]
        embeddings = self.model.encode(texts).tolist()

        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=[{"page": c["page"]} for c in chunks],
            ids=[f"id_{i}" for i in range(len(chunks))]
        )

        print("✅ Ingestion Complete")
