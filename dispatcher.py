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

    def process(self, query, data):
        route = self.router.route(query)

        if route == "calculation":
            fsi = self.lookup.calculate_fsi(data["plot_area"])

            parking = self.lookup.parking(fsi["bua"])
            approvals = self.lookup.approvals(data["height"])

            return f"""
### 33(A)(10) Calculation

- Base FSI: {fsi['base']}
- Fungible: {fsi['fungible']}
- Total FSI: {fsi['total']}

➡️ BUA: **{fsi['bua']} sqm**

### Parking
- ECS: {parking['ecs']}
- Visitor: {parking['visitor']}
- Total: {parking['total']}

### Approvals
{chr(10).join(['- ' + a for a in approvals])}
"""

        if route == "rules":
            return """
### Key Rules (33(A)(10))

- Base FSI: ~3.0
- Fungible: up to 35%
- TDR: Allowed subject to conditions
- Parking: As per Table 8B
"""

        # RAG + AI
        docs = self.rag.search(query)

        prompt = f"""
Context:
{docs}

Query:
{query}
"""

        return self.groq.ask(prompt)
