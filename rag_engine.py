import fitz


class RAGEngine:

    def __init__(self):
        self.pdf_path = "data/MUMBAI-DCPR.pdf"

    def search(self, query, top_k=3):
        doc = fitz.open(self.pdf_path)

        results = []

        for page_num, page in enumerate(doc):
            text = page.get_text()

            if query.lower() in text.lower():
                results.append(
                    f"[Page {page_num+1}]\n{text[:800]}"
                )

        return results[:top_k]
