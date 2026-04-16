import streamlit as st
from agent import UDCPRAgent

st.set_page_config(page_title="33(A)(10) AI Agent", layout="wide")

st.title("Mumbai DCPR 33(A)(10) Intelligent Agent")

st.sidebar.header("Project Inputs")

plot_area = st.sidebar.number_input("Plot Area (sqm)", 0.0, 1000.0)
road_width = st.sidebar.number_input("Road Width (m)", 0.0, 12.0)
height = st.sidebar.number_input("Building Height (m)", 0.0, 15.0)

project_data = {
    "plot_area": plot_area,
    "road_width": road_width,
    "height": height,
    "regulation": "33(A)(10)"
}

query = st.text_area("Ask your query")

if st.button("Analyze"):
    agent = UDCPRAgent()
    result = agent.run(query, project_data)
    st.markdown(result)
