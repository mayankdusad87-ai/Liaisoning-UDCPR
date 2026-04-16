class QueryRouter:

    def route(self, query):
        query = query.lower()

        if any(word in query for word in ["calculate", "bua", "area"]):
            return "calculation"

        if any(word in query for word in ["fsi", "setback", "parking"]):
            return "structured_lookup"

        return "rag_search"
