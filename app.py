import streamlit as st
from agent import UDCPRAgent

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(
    page_title="33(A)(10) Liaisoning Agent",
    layout="wide"
)

st.title("Mumbai DCPR 33(A)(10) AI Agent")
st.write("Specialized AI assistant for redevelopment compliance.")

# -----------------------------
# Sidebar Inputs
# -----------------------------
st.sidebar.header("Project Details")

plot_area = st.sidebar.number_input(
    "Plot Area (sqm)",
    min_value=0.0,
    value=1000.0
)

road_width = st.sidebar.number_input(
    "Road Width (m)",
    min_value=0.0,
    value=12.0
)

zone = st.sidebar.selectbox(
    "Zone",
    ["residential", "commercial", "industrial"]
)

height = st.sidebar.number_input(
    "Building Height (m)",
    min_value=0.0,
    value=15.0
)

# ✅ Fixed regulation (hardcoded)
regulation = "33(A)(10)"

# -----------------------------
# Project Data
# -----------------------------
project_data = {
    "plot_area": plot_area,
    "road_width": road_width,
    "zone": zone,
    "height": height,
    "regulation": regulation
}

# -----------------------------
# Query Box
# -----------------------------
query = st.text_area("Ask your query")

# -----------------------------
# Agent Call
# -----------------------------
if st.button("Submit Query"):
    if query.strip():
        agent = UDCPRAgent()
        response = agent.run(query, project_data)

        st.subheader("Response")
        st.markdown(response)  # ✅ better UI than st.write
    else:
        st.warning("Please enter your query.")
