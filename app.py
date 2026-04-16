import streamlit as st
from agent import UDCPRAgent

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(
    page_title="UDCPR AI Liaisoning Agent",
    layout="wide"
)

st.title("UDCPR 2034 Liaisoning Agent")
st.write("AI assistant for FSI, setbacks, clauses and compliance.")

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

regulation = "33(A)(10)"
)

project_data = {
    "plot_area": plot_area,
    "road_width": road_width,
    "zone": zone,
    "height": height,
    "scheme": scheme
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
        st.write(response)
    else:
        st.warning("Please enter your query.")
