import pdfplumber

class RAGEngine:

    def __init__(self):
        self.docs = self.load_docs("data/MUBAI_DCPR.pdf")

    def load_docs(self, path):
        chunks = []

        try:
            with pdfplumber.open(path) as pdf:

                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()

                    if text:
                        paragraphs = text.split("\n\n")

                        for para in paragraphs:
                            if len(para.strip()) > 100:
                                chunks.append({
                                    "text": para.strip(),
                                    "page": i + 1
                                })

        except Exception as e:
            print("PDF Load Error:", e)

        print(f"Loaded {len(chunks)} chunks")
        return chunks

    def search(self, query, top_k=3):

        if not self.docs:
            return []

        query_words = query.lower().split()

        scored = []

        for doc in self.docs:
            text = doc["text"].lower()

            score = sum(1 for word in query_words if word in text)

            if score > 0:
                scored.append((score, doc))

        scored.sort(reverse=True, key=lambda x: x[0])

        results = []

        for score, doc in scored[:top_k]:
            results.append(
                f"[Page {doc['page']}]\n{doc['text']}"
            )

        return results
