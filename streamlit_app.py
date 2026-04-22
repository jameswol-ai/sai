# sai/streamlit_app.py 

import streamlit as st

# Core system
from src.core.engine import WorkflowEngine
from src.core.doc_loader import DocLoader
from src.core.retriever import SimpleRetriever
from src.core.location_resolver import LocationResolver

# -------------------------------
# 🔧 Setup System (runs once)
# -------------------------------
@st.cache_resource
def initialize_engine():
    doc_loader = DocLoader()

    documents = {
        "global": doc_loader.load_doc("docs/building_codes/global_standards.md"),
        "tropical": doc_loader.load_doc("docs/building_codes/tropical_climate.md"),
        "fire": doc_loader.load_doc("docs/building_codes/fire_safety_rules.md"),
    }

    retriever = SimpleRetriever(documents)
    resolver = LocationResolver()

    # Example workflow (you can load from JSON instead)
    workflow = {
        "basic_design": [
            {"name": "concept"},
            {"name": "compliance"},
            {"name": "output"},
        ]
    }

    engine = WorkflowEngine(workflow)

    # Inject intelligence into context
    engine.set_context("retriever", retriever)
    engine.set_context("location_resolver", resolver)
    engine.set_context("building_codes_tropical", documents["tropical"])

    return engine


# -------------------------------
# 🎨 UI Layout
# -------------------------------
st.set_page_config(page_title="AI Architecture Bot", layout="wide")

st.title("🏗️ AI Architecture Bot")
st.caption("Designs that think about climate, rules, and reality")

engine = initialize_engine()

# -------------------------------
# 🧠 User Input
# -------------------------------
user_input = st.text_area(
    "Describe your project:",
    placeholder="e.g. Eco-friendly school in Juba with natural ventilation",
    height=120
)

run_button = st.button("🚀 Generate Design")

# -------------------------------
# ⚙️ Run Workflow
# -------------------------------
if run_button and user_input.strip():
    with st.spinner("Designing... thinking... consulting the code gods 📜"):
        engine.set_context("input", user_input)

        result = engine.run_workflow("basic_design")

    st.success("Design generated!")

    # -------------------------------
    # 📤 Output Sections
    # -------------------------------
    st.subheader("🧠 Concept")
    st.write(result.get("concept", "No concept generated"))

    st.subheader("📏 Compliance")
    st.write(result.get("compliance", "No compliance check"))

    st.subheader("📄 Final Output")
    st.write(result.get("output", "No final output"))

    # -------------------------------
    # 🔍 Debug / Transparency
    # -------------------------------
    with st.expander("🔍 Internal Context (for debugging)"):
        st.json(result)

elif run_button:
    st.warning("Please enter a project description first.")
