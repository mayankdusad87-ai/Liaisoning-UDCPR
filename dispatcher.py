from query_router import QueryRouter
from structured_lookup import StructuredLookup
from groq_client import GroqClient
from rag_engine import RAGEngine


class QueryDispatcher:

    def __init__(self):
        self.router = QueryRouter()
        self.lookup = StructuredLookup()
        self.groq = GroqClient()
        self.rag = RAGEngine()

    def structured_lookup_handler(self, query, project_data):
        query = query.lower()

        if "fsi" in query:
            fsi = self.lookup.get_fsi(
                project_data["zone"],
                project_data["road_width"]
            )
            return f"Applicable FSI = {fsi}"

        if "setback" in query:
            setback = self.lookup.get_setback(
                project_data["height"]
            )
            return (
                f"Required setbacks:\n"
                f"Front = {setback['front']} m\n"
                f"Side = {setback['side']} m\n"
                f"Rear = {setback['rear']} m"
            )

        return "No structured rule found."

    def calculation_handler(self, query, project_data):
        plot_area = project_data["plot_area"]

        fsi = self.lookup.get_fsi(
            project_data["zone"],
            project_data["road_width"]
        )

        bua = plot_area * fsi

        return f"Permissible built-up area = {bua} sqm"

    def rag_handler(self, query, project_data):
        docs = self.rag.search(query)

        context = "\n\n".join(docs)

        prompt = f"""
Use only the following UDCPR clauses:

{context}

Answer the user query with clause references.

Query: {query}
"""

        return self.groq.ask(prompt)

    def process(self, query, project_data):
        route = self.router.route(query)

        if route == "structured_lookup":
            return self.structured_lookup_handler(query, project_data)

        elif route == "calculation":
            return self.calculation_handler(query, project_data)

        elif route == "rag_search":
            return self.rag_handler(query, project_data)

        return "Unable to process query."
