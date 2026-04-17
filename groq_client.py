from groq import Groq
import streamlit as st


class GroqClient:

    def __init__(self):
        api_key = st.secrets["GROQ_API_KEY"]
        self.client = Groq(api_key=api_key)

        self.system_prompt = """
You are a senior Mumbai DCPR liaisoning consultant,
specialized in Regulation 33(A)(10) redevelopment.

You MUST follow this structure:

### 1. Applicable Clause / Rule
- Refer to relevant DCPR clause or regulation
- If clause not found in context, say: "Clause reference requires verification"

### 2. Calculation / Compliance Logic
- Show step-by-step reasoning
- Use project inputs where applicable

### 3. FSI / TDR / Fungible Impact
- Mention base FSI
- Mention fungible FSI (typically up to 35%)
- Mention TDR applicability if relevant

### 4. Required Approvals / NOCs
- Fire NOC (>24m)
- Environmental clearance (if applicable)
- Any authority-specific approvals

### 5. Final Recommendation
- Clear professional advice
- Mention assumptions explicitly

Strict Rules:
- DO NOT guess clause numbers
- ALWAYS prioritize given context over general knowledge
- If context is missing → clearly state assumptions
- If data is insufficient → say "insufficient data for exact compliance"
"""

    def ask(self, query, project_data=None, context=None):

        # -----------------------------
        # Project Context
        # -----------------------------
        project_info = ""
        if project_data:
            project_info = f"""
Project Details:
- Plot Area: {project_data.get('plot_area')}
- Road Width: {project_data.get('road_width')}
- Height: {project_data.get('height')}
- Regulation: 33(A)(10)
"""

        # -----------------------------
        # RAG Context
        # -----------------------------
        rag_context = ""

        if context and len(context.strip()) > 50:
            rag_context = f"""
Relevant DCPR Extract (USE THIS FIRST):
{context}
"""
        else:
            rag_context = """
No direct clause retrieved from DCPR database.

Use general 33(A)(10) knowledge.
Clearly mention assumptions.
"""

        #
