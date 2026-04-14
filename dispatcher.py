from query_router import QueryRouter

class QueryDispatcher:

    def __init__(self):
        self.router = QueryRouter()

    def structured_lookup_handler(self, query, project_data):
        return "Structured lookup engine response."

    def calculation_handler(self, query, project_data):
        plot_area = project_data["plot_area"]
        fsi = 1.2
        bua = plot_area * fsi

        return f"Permissible built-up area = {bua} sqm"

    def rag_handler(self, query, project_data):
        return "Clause search / legal RAG response."

    def process(self, query, project_data):
        route = self.router.route(query)

        if route == "structured_lookup":
            return self.structured_lookup_handler(query, project_data)

        elif route == "calculation":
            return self.calculation_handler(query, project_data)

        elif route == "rag_search":
            return self.rag_handler(query, project_data)

        return "Unable to process query."
