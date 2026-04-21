def process(self, query, data):

    try:
        # -----------------------------------
        # SAFETY CHECK
        # -----------------------------------
        if not query or not query.strip():
            return "Please enter a valid query."

        route = self.router.route(query)
        print("ROUTE:", route)

        scheme = data.get("scheme", "33A10")

        # -----------------------------------
        # CALCULATION ENGINE
        # -----------------------------------
        if route == "calculation":

            fsi = self.rules.calculate_fsi(data["plot_area"], scheme)

            parking = self.rules.calculate_parking(fsi["bua"], scheme)

            approvals = self.rules.check_approvals(data["height"], scheme)

            response = self.groq.ask(
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

            return response if response else "No response generated."

        # -----------------------------------
        # RAG + CLAUSE INTELLIGENCE
        # -----------------------------------
        docs = self.rag.search(query)

        context = "\n\n".join(docs) if docs else ""

        response = self.groq.ask(
            query=query,
            project_data=data,
            context=context if context else """
No exact clause found in DCPR extract.
Answer based on general Regulation 33(A)(10) understanding.
"""
        )

        return response if response else "No response generated."

    except Exception as e:
        return f"Error occurred: {str(e)}"
