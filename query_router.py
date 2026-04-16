class QueryRouter:

    def __init__(self):
        # Expanded keywords with synonyms
        self.lookup_keywords = [
            "fsi", "floor space index",
            "setback", "margin",
            "parking", "car parking", "ecs",
            "road width",
            "premium fsi"
        ]

        self.calculation_keywords = [
            "calculate", "calculation",
            "built up area", "bua",
            "permissible area",
            "how much", "total", "maximum buildable"
        ]

        self.legal_keywords = [
            "clause", "regulation", "rule",
            "noc", "approval",
            "allowed", "permitted",
            "requirement", "condition",
            "can i", "is it allowed"
        ]

    def route(self, query):
        query = query.lower()

        scores = {
            "structured_lookup": 0,
            "calculation": 0,
            "rag_search": 0
        }

        # scoring logic
        for keyword in self.lookup_keywords:
            if keyword in query:
                scores["structured_lookup"] += 2   # higher weight

        for keyword in self.calculation_keywords:
            if keyword in query:
                scores["calculation"] += 3   # highest priority

        for keyword in self.legal_keywords:
            if keyword in query:
                scores["rag_search"] += 2

        # 🔥 Priority override logic

        # If calculation intent is detected strongly → force calculation
        if scores["calculation"] >= 3:
            return "calculation"

        # If lookup intent strong
        if scores["structured_lookup"] >= 2:
            return "structured_lookup"

        # If legal query detected
        if scores["rag_search"] >= 2:
            return "rag_search"

        # 🔥 fallback (VERY IMPORTANT)
        return "rag_search"
