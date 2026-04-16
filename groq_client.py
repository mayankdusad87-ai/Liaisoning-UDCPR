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
- If unsure, clearly say "Clause reference requires verification"

### 2. Calculation / Compliance Logic
- Show step-by-step reasoning
- Use project inputs where required

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
- Always refer to 33(A)(10) context
- If data is missing → state assumptions
- Prefer given context over general knowledge
"""

    def ask(self, query, project_data=None, context=None):
        """
        query: user question
        project_data: dict (plot_area, road_width, height, etc.)
        context: RAG extracted text
        """

        # Build structured input
        project_info = ""
        if project_data:
            project_info = f"""
Project Details:
- Plot Area: {project_data.get('plot_area')}
- Road Width: {project_data.get('road_width')}
- Height: {project_data.get('height')}
- Regulation: 33(A)(10)
"""

        rag_context = ""
        if context:
            rag_context = f"""
Relevant DCPR Extract:
{context}
"""

        final_prompt = f"""
{project_info}

{rag_context}

User Query:
{query}
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": final_prompt
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content
