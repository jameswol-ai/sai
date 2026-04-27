import streamlit as st
import sys
import os
import traceback

# --------------------------------------------------
# 🧭 FIX PATH (CRITICAL)
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(BASE_DIR, "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

# --------------------------------------------------
# 🎛 UI
# --------------------------------------------------
st.set_page_config(page_title="AI Architecture Bot", layout="wide")

st.title("🏗️ AI Architecture Bot")

# --------------------------------------------------
# 🧠 IMPORT (STANDARDIZED)
# --------------------------------------------------
try:
    from core.engine import WorkflowEngine
except Exception:
    st.error("❌ Failed to import WorkflowEngine")
    st.code(traceback.format_exc())
    st.stop()

# --------------------------------------------------
# 🧩 FUNCTIONS
# --------------------------------------------------
def concept_stage(ctx):
    return f"Concept: {ctx.get('input')}"

def climate_stage(ctx):
    if "tropical" in ctx.get("input", "").lower():
        return "🌴 Tropical design applied"
    return "Standard climate design"

def eco_stage(ctx):
    if "eco" in ctx.get("input", "").lower():
        return "♻️ Eco features added"
    return "No eco features"

def final_output(ctx):
    return f"""
FINAL DESIGN

Concept:
{ctx.get('concept')}

Climate:
{ctx.get('climate')}

Eco:
{ctx.get('eco')}
"""

function_registry = {
    "concept_stage": concept_stage,
    "climate_stage": climate_stage,
    "eco_stage": eco_stage,
    "final_output": final_output,
}

# --------------------------------------------------
# 🗺 WORKFLOW
# --------------------------------------------------
workflow = {
    "design_flow": [
        {"name": "concept_stage", "output_key": "concept"},
        {"name": "climate_stage", "output_key": "climate"},
        {"name": "eco_stage", "output_key": "eco"},
        {"name": "final_output", "output_key": "result"},
    ]
}

# --------------------------------------------------
# ⚙️ ENGINE
# --------------------------------------------------
engine = WorkflowEngine(workflow, function_registry)

# --------------------------------------------------
# 🎯 INPUT
# --------------------------------------------------
user_input = st.text_area(
    "Describe your architectural project:",
    placeholder="Eco-friendly school in tropical climate"
)

# --------------------------------------------------
# ▶️ RUN
# --------------------------------------------------
if st.button("Generate Design"):
    if not user_input.strip():
        st.warning("Please enter a project description")
    else:
        try:
            engine.set_context("input", user_input)
            result = engine.run_workflow("design_flow")

            st.success("✅ Design Generated")

            st.subheader("Output")
            st.code(result.get("result", "No result"))

            with st.expander("Full Context"):
                st.json(result)

        except Exception:
            st.error("❌ Runtime error")
            st.code(traceback.format_exc())
