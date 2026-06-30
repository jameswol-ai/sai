# =========================================================
# ARC — ARCHITECTURAL INTELLECT ENGINE (FIXED)
# Generative Multi-Story Floor Plan & Structural Synthesis
# =========================================================

import streamlit as st
import json
import uuid
import random
import math
from pathlib import Path
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Arc Studio Engine",
    page_icon="📐",
    layout="wide"
)

MEMORY_FILE = Path("arc_studio_v11.json")

# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>
html, body {
    font-family: 'Arial';
    background: #050814;
    color: white;
}

h1, h2, h3 {
    color: #38bdf8;
}

.arc-blueprint-canvas {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 12px;
    padding: 20px;
}

.arc-room-module {
    padding: 16px;
    border-radius: 10px;
    border: 1px solid #1e293b;
}

.room-title {
    font-weight: bold;
    margin-bottom: 5px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MEMORY
# =========================================================

DEFAULT_STATE = {"designs": [], "logs": []}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.load(open(MEMORY_FILE))
        except:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory():
    try:
        json.dump(st.session_state.memory, open(MEMORY_FILE, "w"), indent=2)
    except:
        pass

def log_event(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "active_design" not in st.session_state:
    st.session_state.active_design = None

mem = st.session_state.memory

# =========================================================
# ARCH TYPES
# =========================================================

ARCH_DOMAINS = {
    "Residential": ["Luxury Villa", "Modern Apartment"],
    "Commercial": ["Office Block", "Clinic Center"],
    "Industrial": ["Warehouse", "Factory"]
}

# =========================================================
# GENERATOR
# =========================================================

def generate_spatial_model(domain, btype, plot_size, floors, baths):

    max_fp = int(plot_size * 0.65)
    floor_area = random.randint(120, max_fp)
    total_gfa = floor_area * floors

    span = 6.0 if domain == "Residential" else 7.5 if domain == "Commercial" else 12.0

    col_count = max(12, int((floor_area / 100)))
    beam_count = int(col_count * 1.8)

    rooms = [
        {"name": "Lobby", "type": "Core", "w": 3, "h": 8, "color": "#1e293b"}
    ]

    if domain == "Residential":
        bedrooms = max(1, total_gfa // 120)
        for i in range(bedrooms):
            rooms.append({
                "name": f"Bedroom {i+1}",
                "type": "Room",
                "w": 4,
                "h": 4,
                "color": "#2a0f4d"
            })

    elif domain == "Commercial":
        rooms.append({"name": "Office Floor", "type": "Work", "w": 10, "h": 8, "color": "#075e8a"})

    else:
        rooms.append({"name": "Production Hall", "type": "Industrial", "w": 14, "h": 10, "color": "#3b0764"})

    for i in range(baths):
        rooms.append({
            "name": f"Bath {i+1}",
            "type": "Service",
            "w": 3,
            "h": 2,
            "color": "#4a2306"
        })

    return {
        "id": str(uuid.uuid4())[:8],
        "domain": domain,
        "type": btype,
        "plot_size": plot_size,
        "floors": floors,
        "total_gfa": total_gfa,
        "rooms": rooms,
        "doors": len(rooms),
        "windows": int(total_gfa / 20),
        "structural": {
            "columns": col_count * floors,
            "beams": beam_count * floors,
            "span": span
        }
    }

# =========================================================
# FLOOR PLAN
# =========================================================

def generate_floor_plan(d):
    return d["rooms"]

# =========================================================
# RENDER
# =========================================================

def render(plan):
    html = '<div class="arc-blueprint-canvas">'
    for r in plan:
        html += f"""
        <div class="arc-room-module" style="background:{r['color']}">
            <div class="room-title">{r['name']}</div>
            <div>{r['w']}m x {r['h']}m</div>
        </div>
        """
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# =========================================================
# EUROCODE (FIXED)
# =========================================================

def eurocode(d):

    span = d["structural"]["span"]

    gk = 5.5
    qk = 2.0

    load = (1.35 * gk) + (1.5 * qk)
    w_ed = load * 4.5

    m_ed = (w_ed * span**2) / 8
    m_rd = (0.167 * 30 * 300 * (450**2)) / 1e6

    return {
        "MEd": round(m_ed, 2),
        "MRd": round(m_rd, 2),
        "STATUS": "PASS" if m_rd > m_ed else "FAIL"
    }

# =========================================================
# UI
# =========================================================

st.sidebar.title("ARC V11")
page = st.sidebar.radio("Menu", ["Dashboard", "Generate"])

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("ARC SYSTEM")

    c1, c2 = st.columns(2)
    c1.metric("Designs", len(mem["designs"]))
    c2.metric("Logs", len(mem["logs"]))

# =========================================================
# GENERATION
# =========================================================

elif page == "Generate":

    st.title("Generate Structure")

    domain = st.selectbox("Domain", list(ARCH_DOMAINS.keys()))
    btype = st.selectbox("Type", ARCH_DOMAINS[domain])

    plot = st.slider("Plot Size", 200, 3000, 800)
    floors = st.slider("Floors", 1, 10, 3)
    baths = st.slider("Bathrooms", 1, 6, 2)

    if st.button("Generate"):

        asset = generate_spatial_model(domain, btype, plot, floors, baths)
        asset["plan"] = generate_floor_plan(asset)

        mem["designs"].append(asset)
        log_event("Generated structure")

        st.success("Generated!")

        st.json(asset)

        st.subheader("Floor Plan")
        render(asset["plan"])

        st.subheader("Eurocode Check")
        st.json(eurocode(asset))
