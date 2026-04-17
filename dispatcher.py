from query_router import QueryRouter
from rule_engine import RuleEngine
from groq_client import GroqClient
from rag_engine import RAGEngine


class QueryDispatcher:

    def __init__(self):
        self.router = QueryRouter()
        self.rules = RuleEngine()
        self.groq = GroqClient()
        self.rag = RAGEngine()

    def process(self, query, data):

        # -----------------------------------
        # SAFETY CHECK
        # -----------------------------------
        if not query or not query.strip():
            return "Please enter a valid query."

        route = self.router.route(query)

        scheme = data.get("scheme", "33A10")

        # -----------------------------------
        # CALCULATION ENGINE (CORE LOGIC)
        # -----------------------------------
        if route == "calculation":

            fsi = self.rules.calculate_fsi(
                data["plot_area"],
                scheme
            )

            parking = self.rules.calculate_parking(
                fsi["bua"],
                scheme
            )

            approvals = self.rules.check_approvals(
                data["height"],
                scheme
            )

            return self.groq.ask(
                query=query,
                project_data=data,
                context=f"""
Computed Compliance Data (Regulation 33(A)(10)):

FSI Calculation:
- Base FSI: {fsi['base']}
- Fungible FSI: {fsi['fungible']}
- Total FSI: {fsi['total']}
- Permissible Built-up Area (BUA): {fsi['bua']} sqm

Parking Requirement:
- ECS Required: {parking['ecs']}
- Visitor Parking: {parking['visitor']}
- Total Parking: {parking['total']}

Approvals Required:
{chr(10).join(['- ' + a for a in approvals])}
"""
            )

        # -----------------------------------
        # RAG + CLAUSE INTELLIGENCE
        # -----------------------------------
        docs = self.rag.search(query)

        # fallback if no docs
        if not docs:
            return self.groq.ask(
                query=query,
                project_data=data,
                context="""
No exact clause found in DCPR extract.

Answer based on general Regulation 33(A)(10) understanding.
Clearly mention assumptions.
"""
            )

        context = "\n\n".join(docs)

        return self.groq.ask(
            query=query,
            project_data=data,
            context=context
        )
