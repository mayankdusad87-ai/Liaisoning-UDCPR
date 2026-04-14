import fitz
import chromadb
from sentence_transformers import SentenceTransformer


class PDFIngestion:

    def __init__(self):
        self.embedder = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.client = chromadb.PersistentClient(
            path="./vector_db"
        )

        self.collection = self.client.get_or_create_collection(
            "udcpr"
        )

    def ingest_pdf(self, pdf_path):
        doc = fitz.open(pdf_path)

        chunks = []

        for page_num, page in enumerate(doc):
            text = page.get_text()

            paragraphs = text.split("\n\n")

            for para in paragraphs:
                para = para.strip()

                if len(para) > 100:
                    chunks.append({
                        "text": para,
                        "page": page_num + 1
                    })

        texts = [c["text"] for c in chunks]

        embeddings = self.embedder.encode(
            texts
        ).tolist()

        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=[
                {"page": c["page"]}
                for c in chunks
            ],
            ids=[
                f"chunk_{i}"
                for i in range(len(chunks))
            ]
        )


if __name__ == "__main__":
    ingestor = PDFIngestion()
    ingestor.ingest_pdf("data/udcpr_2034.pdf")
    print("PDF successfully indexed.")
