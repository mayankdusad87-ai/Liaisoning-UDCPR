import fitz

class RAGEngine:

    def __init__(self):
        self.pdf_path = "data/MUMBAI-DCPR.pdf"

    def search(self, query):
        doc = fitz.open(self.pdf_path)

        results = []

        for i, page in enumerate(doc):
            text = page.get_text()

            if query.lower() in text.lower():
                results.append(f"[Page {i+1}]\n{text[:500]}")

        return results[:3]
