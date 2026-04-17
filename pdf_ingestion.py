import pdfplumber

class PDFIngestion:

    def __init__(self):
        self.docs = []

    def ingest(self, pdf_path):

        with pdfplumber.open(pdf_path) as pdf:

            for i, page in enumerate(pdf.pages):
                text = page.extract_text()

                if text:
                    paragraphs = text.split("\n\n")

                    for para in paragraphs:
                        if len(para.strip()) > 120:
                            self.docs.append({
                                "text": para.strip(),
                                "page": i + 1
                            })

        print(f"Loaded {len(self.docs)} chunks")
        return self.docs
