import streamlit as st
from agent import UDCPRAgent

st.set_page_config(page_title="DCPR AI", layout="wide")

st.title("Mumbai DCPR 33(A)(10) AI Agent")

st.sidebar.header("Project Inputs")

plot_area = st.sidebar.number_input("Plot Area", 0.0, 1000.0)
road_width = st.sidebar.number_input("Road Width", 0.0, 12.0)
height = st.sidebar.number_input("Height", 0.0, 15.0)

data = {
    "plot_area": plot_area,
    "road_width": road_width,
    "height": height,
    "regulation": "33(A)(10)"
}

query = st.text_area("Ask your query")

if st.button("Run"):
    agent = UDCPRAgent()
    result = agent.run(query, data)

    st.markdown(result))
