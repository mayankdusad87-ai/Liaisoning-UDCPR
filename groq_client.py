from groq import Groq
import streamlit as st


class GroqClient:

    def __init__(self):
        api_key = st.secrets["GROQ_API_KEY"]
        self.client = Groq(api_key=api_key)

    def ask(self, prompt):
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
You are a senior liaisoning and UDCPR compliance consultant.

Always respond in the following format:

1. Applicable Clause / Rule
2. Calculation / Compliance Logic
3. FSI / TDR / Fungible Impact
4. Required Approvals / NOCs
5. Final Recommendation

Always mention assumptions and cite rule references whenever possible.
"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content
