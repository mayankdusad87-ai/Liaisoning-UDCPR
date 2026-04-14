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
                    "content": "You are an expert UDCPR compliance assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content
