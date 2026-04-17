import fitz
from sentence_transformers import SentenceTransformer
import chromadb

class PDFIngestion:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection("dcpr")

    def ingest(self, pdf_path):
        doc = fitz.open(pdf_path)

        chunks = []

        for i, page in enumerate(doc):
            text = page.get_text()

            # simple chunking
            for para in text.split("\n\n"):
                if len(para.strip()) > 100:
                    chunks.append({
                        "text": para.strip(),
                        "page": i + 1
                    })

        texts = [c["text"] for c in chunks]
        embeddings = self.model.encode(texts).tolist()

        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=[{"page": c["page"]} for c in chunks],
            ids=[f"id_{i}" for i in range(len(chunks))]
        )

        print("✅ PDF Ingested Successfully")
