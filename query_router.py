class QueryRouter:

    def __init__(self):
        self.lookup_keywords = [
            "fsi",
            "setback",
            "parking",
            "road width",
            "premium fsi"
        ]

        self.calculation_keywords = [
            "calculate",
            "built up area",
            "bua",
            "permissible area"
        ]

        self.legal_keywords = [
            "clause",
            "regulation",
            "rule",
            "noc",
            "approval"
        ]

    def route(self, query):
        query = query.lower()

        scores = {
            "structured_lookup": 0,
            "calculation": 0,
            "rag_search": 0
        }

        for keyword in self.lookup_keywords:
            if keyword in query:
                scores["structured_lookup"] += 1

        for keyword in self.calculation_keywords:
            if keyword in query:
                scores["calculation"] += 1

        for keyword in self.legal_keywords:
            if keyword in query:
                scores["rag_search"] += 1

        return max(scores, key=scores.get)
