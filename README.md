# 🏗️ UDCPR AI Consultant
### Real Estate Liaisoning Tool — UDCPR 2034 | Maharashtra DCR | MRTP

---

## What this does
AI-powered urban development regulation consultant for Maharashtra.  
Uses **Groq (llama-3.3-70b)** for fast, accurate UDCPR 2034 answers.

---

## Setup (5 minutes)

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Get a FREE Groq API Key
- Go to: https://console.groq.com
- Sign up → API Keys → Create Key
- Copy the key (starts with `gsk_...`)

### 3. Run the app
```bash
streamlit run app.py
```

App opens at: **http://localhost:8501**

---

## How to use

1. **Paste your Groq API key** in the sidebar
2. Go to **➕ New Project** — fill in plot details + your query
3. Hit **Get AI Analysis** — instant UDCPR response
4. All projects + queries are **saved locally** in `projects.json`
5. Go to **📋 All Projects** to view history and ask follow-up queries

---

## What the AI answers

| Topic | Examples |
|---|---|
| FSI & Fungible FSI | Base FSI, Premium FSI, road-width linked FSI |
| Setbacks & Margins | Front, side, rear — height-based |
| Height Restrictions | Shadow angle, AAI, fire NOC triggers |
| Parking Norms | Stilt, mechanical, basement |
| TDR / Premium | Receivability, loading limits |
| Zoning & Land Use | Permissible uses, conditional uses |
| Amenity & Recreation | Open space, garden, amenity floor norms |

---

## Tech stack
- **Frontend**: Streamlit
- **LLM**: Groq API — llama-3.3-70b-versatile
- **Storage**: Local JSON file (`projects.json`)
- **Deploy**: Works on localhost or any server (Streamlit Cloud, Railway, etc.)

---

## Deploy to Streamlit Cloud (optional)
1. Push to GitHub
2. Go to https://share.streamlit.io
3. Connect your repo, set `app.py` as entry point
4. Add `GROQ_API_KEY` in Secrets if you want it pre-filled

---

## File structure
```
udcpr_app/
├── app.py              # Main Streamlit app
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── projects.json       # Auto-created when you save first project
```
