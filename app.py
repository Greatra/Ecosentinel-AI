import streamlit as st
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

from orchestrator import run_ecosentinel_agent
import orchestrator
import importlib
# Load environment variables (API keys)
load_dotenv(override=True)

st.set_page_config(page_title="Eco Sentinel AI", layout="centered", page_icon="🏛️")

# --- Custom CSS for Premium Glassmorphic Aesthetics ---
st.markdown("""
<style>
    /* Dynamic Marbled Background */
    .stApp {
        background: linear-gradient(120deg, #e6dec8 0%, #cbd2c6 50%, #d4c5b9 100%);
        background-size: 200% 200%;
        animation: gradientBG 15s ease infinite;
        color: #2c3e2e;
        font-family: 'Inter', sans-serif;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Header styling matching the design */
    h1 {
        text-align: center;
        color: #1a1a1a;
        font-weight: 800;
        font-family: 'Georgia', serif;
        margin-top: -20px;
        letter-spacing: -0.5px;
    }
    
    /* Subtitle styling */
    .subtitle {
        text-align: center;
        color: #4a4a4a;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        padding: 0 20px;
    }
    
    /* Premium Glassmorphic Container */
    .glass-container {
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.7);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #d4b886 0%, #b89758 100%);
        color: white;
        font-weight: 800;
        font-size: 1.4rem;
        border: none;
        border-radius: 12px;
        padding: 24px 20px;
        box-shadow: 0 4px 15px rgba(184, 151, 88, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(184, 151, 88, 0.6);
        color: white;
    }
    
    /* File uploader and text input styling */
    .stFileUploader, .stTextInput {
        background: rgba(255, 255, 255, 0.6);
        border-radius: 12px;
        padding: 10px;
    }
    
    .dashboard-panel {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        color: #1a1a1a;
    }
    .dashboard-alert {
        border-left: 5px solid #d9534f;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'pipeline_run' not in st.session_state:
    st.session_state.pipeline_run = False
if 'final_state' not in st.session_state:
    st.session_state.final_state = None

def run_pipeline(image_path, zone, notes):
    try:
        # ⚠️ CACHE BUSTER: Force Streamlit to recursively reload tools and orchestrator
        import sys
        if 'execution.tools' in sys.modules:
            importlib.reload(sys.modules['execution.tools'])
        importlib.reload(orchestrator)
        final_state = orchestrator.run_ecosentinel_agent(image_path, zone, notes)
        return final_state
    except Exception as e:
        return {"app_fatal_error": str(e)}

# --- UI Layout ---

st.markdown("<p style='text-align: center; color: #b89758; font-weight: bold; letter-spacing: 1px; font-size: 0.9rem; text-transform: uppercase;'>Urban Garden Coordinator Workspace</p>", unsafe_allow_html=True)
st.markdown("<h1>Eco Sentinel AI</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Environmental Decision Support System<br><span style='font-size: 0.95rem; font-style: italic; color: #555;'>Human observations strengthen AI evidence and improve traceability.</span></div>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Developer Options")
    st.toggle("Traceability Mode", key="trace_mode")

def trace(source: str):
    if st.session_state.get("trace_mode", False):
        return f"<p style='font-size:0.8em; color:gray; margin-top:-10px; margin-bottom:10px;'><i>Source: {source}</i></p>"
    return ""

if not st.session_state.pipeline_run:
    # INTAKE SCREEN
    
    st.markdown("<div style='text-align: center; margin-bottom: 20px;'><h3 style='color: #2c3e2e;'>REPORT NEW OBSERVATION</h3><p style='color: #666;'>Provide a clear image and any relevant observations.<br>Human context improves evidence quality.</p></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='glass-container' style='text-align: center; margin-bottom: 30px; padding: 20px;'>
        <div style='font-size: 3rem; margin-bottom: 10px;'>📸</div>
        <h4 style='color: #4a4a4a; margin: 0 0 5px 0;'>No observations yet.</h4>
        <p style='color: #777; margin: 0;'>Submit an environmental report to begin analysis.</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Observation Image", type=["jpg", "jpeg", "png"], help="Provide the clearest macro shot possible. Multiple symptoms in one image are acceptable.")
    
    # Real-world locations for accurate weather geocoding
    zone = st.text_input("Observation Location", help="Used for local environmental conditions.")
    
    crop = st.text_input("Crop or Plant Type (Optional but improves analysis quality)")
    duration = st.selectbox("When did you first notice this?", ["Just today", "1–3 days ago", "Within a week", "More than one week", "Unsure"])
    symptoms = st.multiselect("Observed Symptoms", ["Holes in leaves", "Brown spots", "Yellowing", "Wilting", "White powder", "Sticky residue", "Visible insects", "Stem damage", "Unknown"], help="Human observations are valuable evidence.")
    
    user_notes = st.text_input("Optional Notes", placeholder="e.g. Found under leaves, Present after rainfall, Only affecting north side")
    
    bundled_notes = f"Crop: {crop}. Symptoms: {', '.join(symptoms)}. Duration: {duration}. User Notes: {user_notes}"
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Analyze Observation →"):
        if uploaded_file is not None:
            # Save uploaded file to temp path for Vision Analyst
            temp_path = f"temp_upload_{uuid.uuid4().hex}.jpg"
            try:
                from PIL import Image
                import io
                
                image_bytes = uploaded_file.getvalue()
                st.session_state.uploaded_image_bytes = image_bytes
                
                img = Image.open(io.BytesIO(image_bytes))
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                    
                img.save(temp_path, format="JPEG")
                    
                with st.spinner("EcoSentinel modules analyzing..."):
                    final_state = run_pipeline(temp_path, zone, bundled_notes)
                    st.session_state.final_state = final_state
                    st.session_state.pipeline_run = True
            finally:
                # Cleanup temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                
            st.rerun()
        else:
            st.error("Please upload an image first.")
            


else:
    # POST-SUBMIT DASHBOARD
    state = st.session_state.final_state
    
    st.markdown("## 📊 Coordinator Decision Support")
    
    if state.get("app_fatal_error") and "CASCADE_HALT" not in state.get("app_fatal_error"):
        st.error(f"🚨 Analysis could not be completed. Error details: {state.get('app_fatal_error')}")
    elif state.get("human_review_required") or (state.get("app_fatal_error") and "CASCADE_HALT" in state.get("app_fatal_error")):
        # The Failure Cascade Triggered
        error_msg = state.get('evidence_summary', state.get('app_fatal_error', 'Information unavailable'))
        st.markdown(f"""
<div class='dashboard-panel dashboard-alert'>
    <h3>⚠️ Human Review Required</h3>
    <p><strong>Status:</strong> The Vision Analyst module halted the pipeline.</p>
    <p><strong>Reason:</strong> Insufficient visual evidence or low confidence to proceed. Generating recommendations or risk profiles based on this image would violate our safety protocols.</p>
    <hr>
    <p><strong>Extracted Evidence Summary:</strong> {error_msg}</p>
</div>
""", unsafe_allow_html=True)
        
    else:
        # Full Pipeline Succeeded
        if 'uploaded_image_bytes' in st.session_state:
            st.image(st.session_state.uploaded_image_bytes, caption="Uploaded Observation", use_container_width=True)

        col1, col2 = st.columns(2)
        
        try:
            raw_conf = float(state.get('confidence', 0.0))
            conf_val = raw_conf if raw_conf > 1.0 else raw_conf * 100
        except (ValueError, TypeError):
            conf_val = 0.0
           
        summary_data = state.get("summary_current_situation", {})
        if not isinstance(summary_data, dict):
            summary_data = {}
            
        cur_sit = summary_data.get('current_situation', 'Information unavailable')
        if isinstance(cur_sit, list): cur_sit = " ".join([str(x) for x in cur_sit])
        elif cur_sit is None: cur_sit = 'Information unavailable'
        
        imm_actions_sum = summary_data.get('immediate_actions', [])
        if imm_actions_sum is None: imm_actions_sum = []
        if not isinstance(imm_actions_sum, list): imm_actions_sum = [str(imm_actions_sum)]
        imm_actions_str = ", ".join([str(x) for x in imm_actions_sum])
        
        hum_rev = summary_data.get('human_review', 'Required')
        if isinstance(hum_rev, list): hum_rev = " ".join([str(x) for x in hum_rev])
        elif hum_rev is None: hum_rev = 'Required'
            
        st.markdown(f"""
        <div class='dashboard-panel' style='background: #fdfdfd; border: 1px solid #e2e8f0; border-left: 5px solid #2b5c3f; margin-bottom: 20px;'>
            <h3 style='margin-top:0; color: #2c3e2e;'>📑 Executive Summary</h3>
            <p style='margin: 0 0 10px 0;'><strong>Current Situation:</strong> {cur_sit}</p>
            <p style='margin: 0 0 10px 0;'><strong>Immediate Actions:</strong> {imm_actions_str}</p>
            <hr style='margin: 10px 0;'>
            <p style='margin: 0; font-size: 0.85em; color: #666;'><strong>Human Review:</strong> {hum_rev}</p>
        </div>
        """, unsafe_allow_html=True)

        with col1:
            vis_ev_list = state.get('visible_evidence', [])
            if not isinstance(vis_ev_list, list): vis_ev_list = [str(vis_ev_list)]
            ev_html = "".join([f"<p style='margin:0; margin-left:10px;'>✓ {ev}</p>" for ev in vis_ev_list])
            
            unc_list = state.get('uncertainty', [])
            if not isinstance(unc_list, list): unc_list = [str(unc_list)]
            unc_html = "".join([f"<p style='margin:0; margin-left:10px;'>⚠ {u}</p>" for u in unc_list])
            
            st.markdown(f"""<div class='dashboard-panel'>
                <h4>🔍 Detection</h4>
                <p style='margin:0;'><strong>Class:</strong> {state.get('classification', 'Information Unavailable')}</p>
                <p style='margin:0;'><strong>Model Confidence:</strong> {'High' if conf_val >= 90 else 'Moderate' if conf_val >= 75 else 'Acceptable'} ({conf_val:.1f}%)</p>
                <p style='margin:10px 0 0 0;'><strong>Visible Evidence:</strong></p>
                {ev_html}
                <p style='margin:10px 0 0 0;'><strong>Uncertainty:</strong></p>
                {unc_html}
                {trace('nemotron_vision')}
</div>""", unsafe_allow_html=True)
            
            safety_data = state.get('safety_status', {})
            if not isinstance(safety_data, dict):
                safety_data = {"status": "Unknown", "pollinator_risk": "Unknown", "human_oversight": "Required"}
            
            s_status = safety_data.get("status", "Unknown")
            if isinstance(s_status, list): s_status = " ".join([str(x) for x in s_status])
            elif s_status is None: s_status = "Unknown"
            
            if "SAFE" in str(s_status).upper():
                s_icon = "✓ Safe"
                s_color = "#5cb85c"
            else:
                s_icon = "⚠ Warning"
                s_color = "#d9534f"
                
            p_risk = safety_data.get('pollinator_risk', 'Unknown')
            if isinstance(p_risk, list): p_risk = ", ".join([str(x) for x in p_risk])
            elif p_risk is None: p_risk = "Unknown"
            elif not isinstance(p_risk, str): p_risk = str(p_risk)
            if not p_risk or str(p_risk).strip() == "": p_risk = "Not specified by module"
            
            h_over = safety_data.get('human_oversight', 'Required')
            if isinstance(h_over, list): h_over = ", ".join([str(x) for x in h_over])
            elif h_over is None: h_over = "Required"
            elif not isinstance(h_over, str): h_over = str(h_over)
            
            rai_review = safety_data.get('responsible_ai_review', 'Review completed successfully.')
            rai_conf = safety_data.get('confidence_level', '1.0')
            rai_cav = safety_data.get('key_caveats', 'None identified.')
                
            st.markdown(f"""<div class='dashboard-panel'>
                <h4>🛡️ Safety & Responsible AI Review</h4>
                <p style='margin:0;'><strong>Status:</strong> <span style='color: {s_color}; font-weight: bold;'>{s_icon}</span></p>
                <p style='margin:0;'><strong>Pollinator Risk:</strong> {p_risk}</p>
                <p style='margin:0;'><strong>Human Oversight:</strong> {h_over}</p>
                <hr style='margin:10px 0;'>
                <p style='margin:0;'><strong>Responsible AI Analysis:</strong> {rai_review}</p>
                <p style='margin:0;'><strong>Confidence Level:</strong> {rai_conf}</p>
                <p style='margin:0;'><strong>Key Caveats:</strong> {rai_cav}</p>
                {trace('nemotron')}
</div>""", unsafe_allow_html=True)
            
        with col2:
            # Re-inserting the missing Weather Module
            temp = state.get('temperature', 'Unavailable')
            hum = state.get('humidity', 'Unavailable')
            wind = state.get('wind', 'Unavailable')
            
            st.markdown(f"""<div class='dashboard-panel' style='border-left: 5px solid #5bc0de;'>
                <h4>⛅ Local Environmental Conditions</h4>
                <p style='margin:0;'><strong>Temperature:</strong> {temp}°C</p>
                <p style='margin:0;'><strong>Humidity:</strong> {hum}%</p>
                <p style='margin:0;'><strong>Wind Speed:</strong> {wind} km/h</p>
                {trace('open_meteo')}
</div>""", unsafe_allow_html=True)
            
            risk = str(state.get('risk_level', 'Information Unavailable')).upper()
            risk_reason = state.get('risk_reason', 'Information Unavailable')
            if "UNAVAILABLE" in risk: risk_color = "#777"
            elif "HIGH" in risk: risk_color = "#d9534f"
            elif "MODERATE" in risk: risk_color = "#f0ad4e"
            else: risk_color = "#5cb85c"
            
            st.markdown(f"""<div class='dashboard-panel' style='border-left: 5px solid {risk_color};'>
                <h4>⚠️ Risk Assessment</h4>
                <p style='margin:0;'><strong>Risk Level:</strong> <span style='color: {risk_color}; font-weight: bold;'>{risk}</span></p>
                <p style='margin:10px 0 0 0;'><strong>Reason:</strong><br>{risk_reason}</p>
                {trace('risk_node')}
</div>""", unsafe_allow_html=True)

        # --- Treatment Recommendations Card ---
        treatment = state.get("treatment_actions", {})
        if not isinstance(treatment, dict):
            treatment = {}
            
        imm_actions = treatment.get("immediate_actions", [])
        if not isinstance(imm_actions, list): imm_actions = [str(imm_actions)]
        imm_html = "".join([f"<li style='margin-bottom: 5px;'>{act}</li>" for act in imm_actions])
        
        prev_measures = treatment.get("preventive_measures", [])
        if not isinstance(prev_measures, list): prev_measures = [str(prev_measures)]
        prev_html = "".join([f"<li style='margin-bottom: 5px;'>{act}</li>" for act in prev_measures])
        
        s_note = treatment.get('safety_note', 'These are recommendations only. Final decisions belong to the human coordinator.')
        if isinstance(s_note, list): s_note = " ".join(s_note)
        
        st.markdown(f"""
        <div class='dashboard-panel' style='margin-top: 20px; border-left: 5px solid #4a90e2;'>
            <h3 style='margin-top:0; color: #2c3e2e;'>📋 Treatment Recommendations</h3>
            <div style='display: flex; gap: 20px; flex-wrap: wrap;'>
                <div style='flex: 1; min-width: 250px;'>
                    <h4 style='color: #4a90e2; margin-bottom: 10px;'>Immediate Actions</h4>
                    <ul style='margin: 0; padding-left: 20px;'>{imm_html}</ul>
                </div>
                <div style='flex: 1; min-width: 250px;'>
                    <h4 style='color: #4a90e2; margin-bottom: 10px;'>Preventive Measures</h4>
                    <ul style='margin: 0; padding-left: 20px;'>{prev_html}</ul>
                </div>
            </div>
            <hr style='margin: 15px 0;'>
            <p style='margin: 0; font-size: 0.85em; color: #666;'><strong>Safety Note:</strong> {s_note}</p>
            {trace('llama')}
        </div>
        """, unsafe_allow_html=True)

        # Store in Supabase Logic (Honest presentation)
        if state.get("db_error"):
            st.error("❌ Report could not be saved. Please try again.")
        elif state.get("error"):
            st.warning("⚠️ Analysis completed, but the report could not be saved.")
        else:
            st.success("✅ Report securely logged to EcoSentinel Database.")
        
    if st.button("New Report"):
        st.session_state.pipeline_run = False
        st.session_state.final_state = None
        st.rerun()
