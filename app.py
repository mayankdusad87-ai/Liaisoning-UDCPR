import streamlit as st
from agent import UDCPRAgent

st.set_page_config(page_title="33(A)(10) AI Agent", layout="wide")

st.title("Mumbai DCPR 33(A)(10) AI Agent")
st.write("Specialized redevelopment compliance assistant.")

st.sidebar.header("Project Details")

plot_area = st.sidebar.number_input("Plot Area (sqm)", 0.0, 1000.0)
road_width = st.sidebar.number_input("Road Width (m)", 0.0, 12.0)

zone = st.sidebar.selectbox(
    "Zone",
    ["residential", "commercial", "industrial"]
)

height = st.sidebar.number_input("Building Height (m)", 0.0, 15.0)

# Fixed regulation
regulation = "33(A)(10)"
st.sidebar.success(f"Regulation: {regulation}")

project_data = {
    "plot_area": plot_area,
    "road_width": road_width,
    "zone": zone,
    "height": height,
    "regulation": regulation
}

query = st.text_area("Ask your query")

if st.button("Submit Query"):
    if query.strip():
        agent = UDCPRAgent()
        response = agent.run(query, project_data)

        st.subheader("Response")
        st.markdown(response)
    else:
        st.warning("Please enter your query.")
