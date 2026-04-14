from groq import Groq
import streamlit as st


class GroqClient:

    def __init__(self):
        api_key = st.secrets["GROQ_API_KEY"]
        self.client = Groq(api_key=api_key)

        self.system_prompt = """
You are a senior liaisoning and UDCPR compliance consultant.

You must always answer in the following structure:

### 1. Applicable Clause / Rule
Mention applicable UDCPR clause, scheme rule, or authority-specific norm.

### 2. Calculation / Compliance Logic
Show calculations clearly step-by-step.

### 3. FSI / TDR / Fungible Impact
Mention base FSI, premium FSI, fungible FSI, and TDR implications.

### 4. Required Approvals / NOCs
Mention fire NOC, environmental, airport, railway, and authority approvals if applicable.

### 5. Final Recommendation
Provide professional liaisoning recommendation with assumptions.

Important:
- Always mention assumptions
- Never guess clause numbers
- Mention if rule depends on scheme (SRA / MHADA / General UDCPR)
"""

    def ask(self, prompt):
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content
