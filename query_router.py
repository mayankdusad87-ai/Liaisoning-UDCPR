class QueryRouter:

    def route(self, query):
        query = query.lower()

        if any(k in query for k in ["calculate", "area", "bua"]):
            return "calculation"

        if any(k in query for k in ["fsi", "parking", "setback"]):
            return "rules"

        return "rag"
