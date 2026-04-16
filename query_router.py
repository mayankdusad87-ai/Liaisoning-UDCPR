class QueryRouter:

    def __init__(self):

        # Intent buckets (much more realistic)
        self.calculation_intent = [
            "calculate", "calculation", "how much",
            "bua", "built up area", "permissible area",
            "total area", "max area"
        ]

        self.explanation_intent = [
            "what", "why", "explain", "meaning",
            "define", "how does", "interpret"
        ]

        self.compliance_intent = [
            "clause", "regulation", "rule",
            "allowed", "permitted", "can i",
            "approval", "noc", "requirement"
        ]

        self.lookup_intent = [
            "fsi", "setback", "margin"
        ]

        self.parking_intent = [
            "parking", "ecs", "car parking"
        ]

    def route(self, query):
        query = query.lower()

        scores = {
            "calculation": 0,
            "rag": 0,
            "rules": 0
        }

        # -----------------------------
        # Detect CALCULATION
        # -----------------------------
        for word in self.calculation_intent:
            if word in query:
                scores["calculation"] += 3

        # -----------------------------
        # Detect EXPLANATION → RAG/AI
        # -----------------------------
        for word in self.explanation_intent:
            if word in query:
                scores["rag"] += 3

        # -----------------------------
        # Detect COMPLIANCE → RAG/AI
        # -----------------------------
        for word in self.compliance_intent:
            if word in query:
                scores["rag"] += 2

        # -----------------------------
        # Detect LOOKUP (simple rules)
        # -----------------------------
        for word in self.lookup_intent:
            if word in query:
                scores["rules"] += 2

        # -----------------------------
        # Parking logic (smart handling)
        # -----------------------------
        if any(word in query for word in self.parking_intent):

            # If user is asking explanation → RAG
            if any(word in query for word in self.explanation_intent):
                scores["rag"] += 3

            # If asking numbers → calculation
            elif any(word in query for word in self.calculation_intent):
                scores["calculation"] += 3

            else:
                scores["rules"] += 2

        # -----------------------------
        # PRIORITY DECISION
        # -----------------------------
        if scores["calculation"] >= 3:
            return "calculation"

        if scores["rag"] >= 2:
            return "rag"

        if scores["rules"] >= 1:
            return "rules"

        # Default fallback (VERY IMPORTANT)
        return "rag"
