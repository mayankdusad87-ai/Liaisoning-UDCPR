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

            # 🔥 Combine with AI explanation
            return self.groq.ask(
                query=query,
                project_data=data,
                context=f"""
Computed Data:
Base FSI: {fsi['base']}
Fungible: {fsi['fungible']}
Total FSI: {fsi['total']}
BUA: {fsi['bua']}

Parking:
ECS: {parking['ecs']}
Visitor: {parking['visitor']}
Total: {parking['total']}

Approvals:
{chr(10).join(approvals)}
"""
            )

        # -----------------------------------
        # STRUCTURED RULES (SMART)
        # -----------------------------------
        if route == "rules":

            return self.groq.ask(
                query=query,
                project_data=data,
                context="""
Key 33(A)(10) Rules:
- Base FSI ~3.0
- Fungible up to 35%
- TDR allowed with conditions
- Parking governed by Table 8B
"""
            )

       # -----------------------------------
# RAG + AI (CORE INTELLIGENCE)
# -----------------------------------
docs = self.rag.search(query)

# ✅ Fallback protection
if not docs:
    return self.groq.ask(
        query=query,
        project_data=data,
        context="""
No exact clause found in DCPR document.

Answer
