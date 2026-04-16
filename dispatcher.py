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
            fsi = self.lookup.get_fsi()
            return f"""
### Regulation 33(A)(10)

- Base FSI: {fsi['base']}
- Fungible FSI: {fsi['fungible_percent']}%
- Max FSI: {fsi['max_with_fungible']}
"""

        if "parking" in query:
            return f"""
### Parking Norms
{self.lookup.get_parking()}
"""

        if "setback" in query:
            return f"""
### Setbacks
{self.lookup.get_setback()}
"""

        if "approval" in query or "noc" in query:
            approvals = self.lookup.get_approvals()
            return "### Required Approvals\n" + "\n".join(
                [f"- {a}" for a in approvals]
            )

        return self.rag_handler(query, project_data)

    def calculation_handler(self, query, project_data):
        fsi = self.lookup.get_fsi()["base"]
        bua = project_data["plot_area"] * fsi

        return f"""
### Calculation

Plot Area: {project_data['plot_area']} sqm  
FSI: {fsi}  

➡️ Permissible BUA: **{bua} sqm**
"""

    def rag_handler(self, query, project_data):
        docs = self.rag.search(query)

        context = "\n\n".join(docs)

        prompt = f"""
Regulation: 33(A)(10)

Project:
- Plot Area: {project_data['plot_area']}
- Road Width: {project_data['road_width']}
- Height: {project_data['height']}

Use these clauses:
{context}

Answer clearly with compliance logic.

Query: {query}
"""

        return self.groq.ask(prompt)

    def process(self, query, project_data):
        route = self.router.route(query)

        if route == "structured_lookup":
            return self.structured_lookup_handler(query, project_data)

        elif route == "calculation":
            return self.calculation_handler(query, project_data)

        return self.rag_handler(query, project_data)
