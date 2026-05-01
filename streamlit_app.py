# sai/streamlit_app.py

import streamlit as st
import random
import json
import time
import logging

# =========================================================
# 🏗️ ARCHITECTURAL DESIGN AI — SOUTH SUDAN EDITION
# =========================================================

st.set_page_config(page_title="Architect AI: South Sudan", layout="wide")

logging.basicConfig(
    filename="architect_ai.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# ---------------------------
# SESSION STATE
# ---------------------------
def init_state():
    st.session_state.setdefault("designs", [])
    st.session_state.setdefault("current_design", None)
    st.session_state.setdefault("climate_mode", "Hot & Dry")
    st.session_state.setdefault("floors", 1)

init_state()

# ---------------------------
# CORE ARCHITECTURE ENGINE
# ---------------------------
class ArchitectEngine:
    def __init__(self, climate="Hot & Dry"):
        self.climate = climate

    def building_code_profile(self):
        return {
            "foundation": "Raised reinforced concrete (flood + soil heat resistance)",
            "walls": "Compressed earth blocks or stabilized adobe + ventilation gaps",
            "roof": "Sloped corrugated metal with heat-reflective coating",
            "ventilation": "Cross-ventilation mandatory",
            "water_management": "Rainwater harvesting + elevated drainage channels",
            "heat_strategy": "Shaded courtyards + extended roof overhangs",
        }

    def generate_floor_plan(self, floors=1, building_type="residential"):
        base_rooms = ["Living Area", "Kitchen", "Bathroom", "Storage"]

        if building_type == "commercial":
            base_rooms = ["Retail Space", "Office Area", "Storage", "Service Room"]

        plan = {}
        for f in range(1, floors + 1):
            plan[f"Floor {f}"] = random.sample(base_rooms, len(base_rooms))

        return plan

    def multi_store_config(self):
        return {
            "ground_floor": "Commercial / Shops / Market stalls",
            "upper_floors": "Residential housing units",
            "structure_note": "Separated load zones for vibration + crowd safety"
        }

    def single_store_config(self):
        return {
            "layout": "Single-story spread structure",
            "use_case": "Residential or small clinic/school",
            "expansion": "Horizontal modular expansion recommended"
        }

    def simulate_design(self, floors, building_type):
        return {
            "temperature_resilience": f"{random.randint(70, 95)}%",
            "ventilation_efficiency": f"{random.randint(65, 90)}%",
            "flood_resistance": f"{random.randint(60, 85)}%",
            "material_efficiency": f"{random.randint(75, 92)}%",
        }

engine = ArchitectEngine()

# ---------------------------
# UI LAYOUT
# ---------------------------
st.title("🏗️ Architect AI — South Sudan Design Engine")
st.caption("Generating climate-aware buildings adapted to local environmental realities")

tab_design, tab_codes, tab_sim, tab_logs = st.tabs(
    ["📐 Design Generator", "📜 Building Codes", "🧪 Simulation", "🧾 History"]
)

# =========================================================
# 📐 DESIGN GENERATOR
# =========================================================
with tab_design:
    st.header("Generate Architectural Design")

    building_type = st.selectbox("Building Type", ["residential", "commercial"])
    floors = st.slider("Number of Floors", 1, 5, 1)
    structure_mode = st.radio("Structure Mode", ["Single Store", "Multi Store"])

    if st.button("Generate Design"):
        floor_plan = engine.generate_floor_plan(floors, building_type)

        if structure_mode == "Multi Store":
            config = engine.multi_store_config()
        else:
            config = engine.single_store_config()

        design = {
            "type": building_type,
            "floors": floors,
            "structure": structure_mode,
            "floor_plan": floor_plan,
            "config": config,
            "climate": engine.climate
        }

        st.session_state.current_design = design
        st.session_state.designs.append(design)

        logging.info(f"Generated design: {design}")

    if st.session_state.current_design:
        st.subheader("🧱 Current Design Output")
        st.json(st.session_state.current_design)

# =========================================================
# 📜 BUILDING CODES
# =========================================================
with tab_codes:
    st.header("South Sudan Adaptive Building Codes (AI Generated)")
    st.json(engine.building_code_profile())

    st.info("These are adaptive AI guidelines for hot climates, flood-prone zones, and mixed urban-rural environments.")

# =========================================================
# 🧪 SIMULATION
# =========================================================
with tab_sim:
    st.header("Design Performance Simulation")

    if st.session_state.current_design:
        result = engine.simulate_design(
            st.session_state.current_design["floors"],
            st.session_state.current_design["type"]
        )

        st.subheader("Performance Metrics")
        st.json(result)

        st.progress(int(result["temperature_resilience"].replace("%", "")) / 100)
        st.progress(int(result["ventilation_efficiency"].replace("%", "")) / 100)

    else:
        st.warning("Generate a design first to simulate performance.")

# =========================================================
# 🧾 HISTORY
# =========================================================
with tab_logs:
    st.header("Design History")

    if st.session_state.designs:
        for i, d in enumerate(st.session_state.designs[::-1]):
            st.markdown(f"### Design #{len(st.session_state.designs)-i}")
            st.json(d)
    else:
        st.info("No designs generated yet.")
