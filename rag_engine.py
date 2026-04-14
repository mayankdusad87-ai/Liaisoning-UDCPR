import fitz


class RAGEngine:

    def __init__(self):
        self.pdf_path = "data/udcpr_2034.pdf"

    def search(self, query, top_k=3):
        doc = fitz.open(self.pdf_path)

        query_words = query.lower().split()

        matches = []

        for page_num, page in enumerate(doc):
            text = page.get_text()

            score = sum(
                1 for word in query_words
                if word in text.lower()
            )

            if score > 0:
                matches.append(
                    {
                        "page": page_num + 1,
                        "text": text[:1000],
                        "score": score
                    }
                )

        matches = sorted(
            matches,
            key=lambda x: x["score"],
            reverse=True
        )

        results = []

        for match in matches[:top_k]:
            results.append(
                f"[Page {match['page']}]\n{match['text']}"
            )

        return results
