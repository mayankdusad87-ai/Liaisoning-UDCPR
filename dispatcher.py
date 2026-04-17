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

        # -----------------------------------
        # CALCULATION ENGINE
        # -----------------------------------
        if route == "calculation":

            fsi = self.lookup.calculate_fsi(data["plot_area"])
            parking = self.lookup.parking(fsi["bua"])
            approvals = self.lookup.approvals(data["height"])

            return self.groq.ask(
                query=query,
                project_data=data,
                context=f"""
Computed Data:

FSI:
- Base: {fsi['base']}
- Fungible: {fsi['fungible']}
- Total: {fsi['total']}
- BUA: {fsi['bua']}

Parking:
- ECS: {parking['ecs']}
- Visitor: {parking['visitor']}
- Total: {parking['total']}

Approvals:
{chr(10).join(approvals)}
"""
            )

        # -----------------------------------
        # RULES (structured + AI)
        # -----------------------------------
        if route == "rules":

            return self.groq.ask(
                query=query,
                project_data=data,
                context="""
Key 33(A)(10) Rules:

- Base FSI approx 3.0
- Fungible FSI up to 35%
- TDR allowed subject to approval
- Parking governed by Table 8B (ECS-based)
"""
            )

        # -----------------------------------
        # RAG (SEMANTIC SEARCH)
        # -----------------------------------
        docs = self.rag.search(query)

        # ✅ SAFETY: no result fallback
        if not docs:
            return self.groq.ask(
                query=query,
                project_data=data,
                context="""
No exact clause found in DCPR database.

Answer based on general UDCPR 33(A)(10) understanding.
Clearly mention assumptions.
"""
            )

        context = "\n\n".join(docs)

        return self.groq.ask(
            query=query,
            project_data=data,
            context=context
        )
