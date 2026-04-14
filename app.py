import streamlit as st
import json
import os
from datetime import datetime
from groq import Groq

# ─── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="UDCPR AI Consultant",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d6a9f 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .main-header h1 { margin: 0; font-size: 1.8rem; }
    .main-header p  { margin: 0.3rem 0 0; opacity: 0.85; font-size: 0.9rem; }

    .project-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.75rem;
        background: white;
        transition: box-shadow 0.2s;
    }
    .project-card:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.1); }

    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 99px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .badge-res  { background:#e8f5e9; color:#2e7d32; }
    .badge-com  { background:#fff3e0; color:#e65100; }
    .badge-ind  { background:#e3f2fd; color:#1565c0; }
    .badge-mix  { background:#f3e5f5; color:#6a1b9a; }
    .badge-oth  { background:#f5f5f5; color:#424242; }

    .ai-box {
        background: #f8f9fa;
        border-left: 4px solid #2d6a9f;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.25rem;
        font-size: 0.9rem;
        line-height: 1.7;
        white-space: pre-wrap;
        margin-top: 0.75rem;
    }

    .stat-box {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .stat-num   { font-size: 2rem; font-weight: 700; color: #1e3a5f; }
    .stat-label { font-size: 0.8rem; color: #666; margin-top: 2px; }

    .query-block {
        background: #fff;
        border: 1px solid #e8e8e8;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }
    .query-label { font-size: 0.75rem; font-weight: 600; color: #888; text-transform: uppercase; }
    .query-text  { font-style: italic; color: #333; margin-top: 2px; }

    div[data-testid="stSidebar"] { background: #f0f4f8; }
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# ─── Constants ─────────────────────────────────────────────────────────────────
PROJECTS_FILE = "projects.json"

SYSTEM_PROMPT = """You are a highly specialized Urban Development Regulation Expert AI trained on:
- UDCPR 2034 (Unified Development Control & Promotion Regulations - Maharashtra)
- Relevant Local DCR (Development Control Regulations)
- Maharashtra Regional and Town Planning Act (MRTP)
- Standard municipal approval practices

Your role is to act as a REAL ESTATE LIAISONING CONSULTANT for a developer.

Always respond in this EXACT format with these 5 sections:

✅ DIRECT ANSWER
Provide a clear, practical answer in simple terms.

📊 CALCULATION / LOGIC
Show how the answer is derived — Base FSI, Premium/TDR applicability, Road width impact, assumptions made.

📜 REGULATION REFERENCE
Quote the exact clause: Regulation number, clause title, short excerpt (max 2-3 lines).
Format: "UDCPR 2034, Regulation X.X – Title: '...'"

⚠️ CONDITIONS / EXCEPTIONS
Highlight special cases, authority discretion, zone-specific variations.

🧠 PRACTICAL INSIGHT
Explain like a liaisoning consultant: what is typically approved in real projects, common workarounds or optimizations, risk areas where file may get stuck.

Rules:
- Always prioritize UDCPR 2034 over older DCR unless location-specific override exists
- If unsure about exact clause, say "Exact clause needs verification"
- Be crisp, technical, and practically usable for filing drawings and approval strategy
- Never skip clause references
- Never give generic textbook explanations"""


# ─── Data persistence ──────────────────────────────────────────────────────────
def load_projects():
    if os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, "r") as f:
            return json.load(f)
    return []

def save_projects(projects):
    with open(PROJECTS_FILE, "w") as f:
        json.dump(projects, f, indent=2)

# ─── Groq API call ─────────────────────────────────────────────────────────────
def ask_groq(project: dict, query: str, api_key: str) -> str:
    client = Groq(api_key=api_key)

    project_details = f"""Project Details:
- Project Name: {project.get('name', 'Not specified')}
- Plot Area: {project.get('area', 'Not specified')} sqm
- Zone: {project.get('zone', 'Not specified')}
- Road Width: {project.get('road', 'Not specified')} m
- Location / Authority: {project.get('location', 'Not specified')}
- Land Type: {project.get('landtype', 'Not specified')}
- Intended Use: {project.get('use', 'Not specified')}
- Building Height: {project.get('height', 'Not specified')} m
- Special Conditions: {project.get('special', 'None')}

User Query: {query}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": project_details}
        ],
        temperature=0.2,
        max_tokens=1500
    )
    return response.choices[0].message.content

# ─── Zone badge helper ─────────────────────────────────────────────────────────
def zone_badge(zone: str) -> str:
    cls = {
        "Residential": "res", "Commercial": "com",
        "Industrial": "ind", "Mixed Use": "mix"
    }.get(zone, "oth")
    return f'<span class="badge badge-{cls}">{zone}</span>'

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/building.png", width=60)
    st.markdown("### UDCPR AI Consultant")
    st.caption("UDCPR 2034 | Maharashtra DCR | MRTP")
    st.divider()

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Get your free key at console.groq.com"
    )
    if api_key:
        st.success("API key set ✓")
    else:
        st.warning("Enter your Groq API key to start")

    st.divider()
    st.markdown("**Navigation**")
    page = st.radio(
        "Go to",
        ["📋 All Projects", "➕ New Project"],
        label_visibility="collapsed"
    )
    st.divider()
    st.caption("Powered by Groq · llama-3.3-70b")

# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>🏗️ Urban Development Regulation Expert</h1>
  <p>Real Estate Liaisoning Consultant · UDCPR 2034 · Maharashtra DCR · MRTP Act</p>
</div>
""", unsafe_allow_html=True)

# ─── Load data ─────────────────────────────────────────────────────────────────
if "projects" not in st.session_state:
    st.session_state.projects = load_projects()

projects = st.session_state.projects

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ALL PROJECTS
# ══════════════════════════════════════════════════════════════════════════════
if page == "📋 All Projects":

    # Stats row
    total_q = sum(len(p.get("queries", [])) for p in projects)
    zones    = len(set(p.get("zone", "") for p in projects if p.get("zone")))
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="stat-box"><div class="stat-num">{len(projects)}</div><div class="stat-label">Total projects</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-box"><div class="stat-num">{total_q}</div><div class="stat-label">Queries answered</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-box"><div class="stat-num">{zones}</div><div class="stat-label">Zones covered</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if not projects:
        st.info("No projects yet. Use **➕ New Project** in the sidebar to add your first project.")
    else:
        # Filter bar
        col_search, col_zone = st.columns([3, 1])
        with col_search:
            search = st.text_input("Search projects", placeholder="Search by name or location...", label_visibility="collapsed")
        with col_zone:
            zone_filter = st.selectbox("Filter by zone", ["All zones", "Residential", "Commercial", "Industrial", "Mixed Use"], label_visibility="collapsed")

        filtered = [
            p for p in reversed(projects)
            if (not search or search.lower() in p.get("name","").lower() or search.lower() in p.get("location","").lower())
            and (zone_filter == "All zones" or p.get("zone") == zone_filter)
        ]

        st.markdown(f"**{len(filtered)} project(s)**")

        for idx, p in enumerate(filtered):
            real_idx = projects.index(p)
            q_count  = len(p.get("queries", []))
            with st.expander(f"📁 {p.get('name','Unnamed')}  —  {p.get('location','N/A')}  ·  {q_count} {'query' if q_count==1 else 'queries'}"):

                # Project metadata grid
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Plot area",    f"{p.get('area','—')} sqm")
                m2.metric("Road width",   f"{p.get('road','—')} m")
                m3.metric("Zone",         p.get('zone','—'))
                m4.metric("Land type",    p.get('landtype','—'))

                m5, m6, m7 = st.columns(3)
                m5.metric("Intended use", p.get('use','—'))
                m6.metric("Height",       f"{p.get('height','—')} m")
                m7.metric("Special",      p.get('special','—') or "None")

                st.divider()

                # Query history
                if q_count:
                    st.markdown("**Query history**")
                    for qi, qa in enumerate(p["queries"]):
                        st.markdown(f"""
                        <div class="query-block">
                          <div class="query-label">Query {qi+1}</div>
                          <div class="query-text">"{qa['question']}"</div>
                          <div class="ai-box">{qa['answer']}</div>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.caption("No queries yet for this project.")

                st.divider()

                # Ask follow-up
                st.markdown("**Ask a follow-up query**")
                follow_q = st.text_area(
                    "Query",
                    placeholder="e.g. What parking is required? Can I use TDR? What height is permissible?",
                    key=f"fq_{real_idx}",
                    label_visibility="collapsed",
                    height=80
                )
                if st.button("Ask AI ↗", key=f"fb_{real_idx}", disabled=not api_key):
                    if follow_q.strip():
                        with st.spinner("Consulting UDCPR 2034 regulations..."):
                            try:
                                answer = ask_groq(p, follow_q.strip(), api_key)
                                if "queries" not in projects[real_idx]:
                                    projects[real_idx]["queries"] = []
                                projects[real_idx]["queries"].append({
                                    "question": follow_q.strip(),
                                    "answer": answer,
                                    "timestamp": datetime.now().isoformat()
                                })
                                save_projects(projects)
                                st.session_state.projects = projects
                                st.rerun()
                            except Exception as e:
                                st.error(f"API error: {e}")
                    else:
                        st.warning("Please enter a query first.")

                if not api_key:
                    st.caption("⚠️ Enter your Groq API key in the sidebar to ask queries.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: NEW PROJECT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "➕ New Project":

    st.subheader("Add a new project")

    with st.form("new_project_form", clear_on_submit=False):
        # Row 1
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Project name *", placeholder="e.g. Shivaji Nagar Plot A")
        with c2:
            location = st.text_input("Location / Authority *", placeholder="e.g. Pune PMC / Thane TMC / PCMC")

        # Row 2
        c1, c2, c3 = st.columns(3)
        with c1:
            area = st.number_input("Plot area (sqm)", min_value=0.0, step=10.0)
        with c2:
            road = st.number_input("Road width (m)", min_value=0.0, step=0.5)
        with c3:
            height = st.number_input("Building height (m, optional)", min_value=0.0, step=1.0)

        # Row 3
        c1, c2, c3 = st.columns(3)
        with c1:
            zone = st.selectbox("Zone *", ["", "Residential", "Commercial", "Industrial", "Mixed Use", "Agricultural"])
        with c2:
            landtype = st.selectbox("Land type", ["", "Freehold", "Leasehold", "NA Plot", "Gaothan", "Government Land"])
        with c3:
            intended_use = st.selectbox("Intended use", ["", "Residential", "Commercial", "Mixed-use", "Institutional", "Industrial"])

        special = st.text_input("Special conditions", placeholder="e.g. Corner plot, CRZ zone, Heritage precinct, Slum rehabilitation...")

        st.divider()
        query = st.text_area(
            "Your query *",
            placeholder="e.g. What is the permissible FSI?\nWhat setbacks are required?\nCan I use TDR on this plot?",
            height=100
        )

        submitted = st.form_submit_button("Get AI Analysis ↗", type="primary", use_container_width=True)

    if submitted:
        errors = []
        if not name.strip():     errors.append("Project name")
        if not location.strip(): errors.append("Location / Authority")
        if not zone:             errors.append("Zone")
        if not query.strip():    errors.append("Your query")
        if not api_key:          errors.append("Groq API key (in sidebar)")

        if errors:
            st.error(f"Please fill in: {', '.join(errors)}")
        else:
            project = {
                "name":     name.strip(),
                "location": location.strip(),
                "area":     str(area) if area else "",
                "road":     str(road) if road else "",
                "height":   str(height) if height else "",
                "zone":     zone,
                "landtype": landtype,
                "use":      intended_use,
                "special":  special.strip(),
                "created":  datetime.now().isoformat(),
                "queries":  []
            }

            with st.spinner("Consulting UDCPR 2034 regulations via Groq..."):
                try:
                    answer = ask_groq(project, query.strip(), api_key)
                    project["queries"].append({
                        "question": query.strip(),
                        "answer":   answer,
                        "timestamp": datetime.now().isoformat()
                    })
                    projects.append(project)
                    save_projects(projects)
                    st.session_state.projects = projects

                    st.success(f"Project **{name}** saved!")
                    st.markdown("### AI Consultant Response")
                    st.markdown(f'<div class="ai-box">{answer}</div>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Groq API error: {e}")
