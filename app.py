import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ===================== PAGE CONFIG =====================
st.set_page_config(page_title="Radioactive Water Contamination Detector", layout="wide")

# ===================== CUSTOM CSS =====================
st.markdown("""
    <style>
    body {
        background-color: #0d0d0d;
        color: white;
        font-family: 'Bebas Neue', sans-serif;
    }

    /* Title Glow */
    .title {
        font-size: 50px;
        text-align: center;
        color: #39ff14;
        text-shadow: 0px 0px 20px #00ff00, 0px 0px 30px #00ff00;
    }

    .subtitle {
        text-align: center;
        font-size: 20px;
        color: #ffea00;
        text-shadow: 0px 0px 10px #ffea00;
    }

    /* Water Drop Animation */
    @keyframes fall {
        0% { transform: translateY(-10vh); opacity: 1; }
        100% { transform: translateY(100vh); opacity: 0; }
    }

    .drops {
        position: fixed;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        pointer-events: none;
        z-index: -1;
        overflow: hidden;
    }

    .drop {
        position: absolute;
        top: -10px;
        font-size: 20px;
        color: #00ffff;
        animation: fall linear infinite;
    }
    </style>
""", unsafe_allow_html=True)

# ===================== BACKGROUND DROPS =====================
st.markdown('<div class="drops">' + ''.join(
    [f'<div class="drop" style="left:{np.random.randint(0,100)}%; animation-duration:{np.random.uniform(3,7)}s; animation-delay:{np.random.uniform(0,5)}s;">💧</div>'
     for _ in range(25)]) + '</div>', unsafe_allow_html=True)

# ===================== HEADER =====================
st.markdown("<h1 class='title'>☢️ Radioactive Water Contamination Detector</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='subtitle'>Futuristic AI/ML Powered System | Developed by Karthikeyan</h3>", unsafe_allow_html=True)

# ===================== SIDEBAR INPUTS =====================
st.sidebar.header("🔍 Enter Water Parameters (Sliders)")
ph_slider = st.sidebar.slider("pH Level", 0.0, 14.0, 7.0)
tds_slider = st.sidebar.slider("TDS (mg/L)", 0, 2000, 300)
hardness_slider = st.sidebar.slider("Hardness (mg/L)", 0, 1000, 200)
nitrate_slider = st.sidebar.slider("Nitrate (mg/L)", 0, 100, 20)

# ===================== CENTER INPUTS =====================
st.markdown("### 🎛️ Manual Input Controls (with +/- buttons)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    ph = st.number_input("pH", min_value=0.0, max_value=14.0, value=ph_slider, step=0.1)
with col2:
    tds = st.number_input("TDS", min_value=0, max_value=2000, value=tds_slider, step=10)
with col3:
    hardness = st.number_input("Hardness", min_value=0, max_value=1000, value=hardness_slider, step=10)
with col4:
    nitrate = st.number_input("Nitrate", min_value=0, max_value=100, value=nitrate_slider, step=1)

# ===================== TABS =====================
tab1, tab2, tab3 = st.tabs(["🧪 Contamination Check + Safety Meter", "📊 Data Overview", "⚠️ Radioactive Awareness"])

# -------- TAB 1: Contamination Check + Safety Meter --------
with tab1:
    st.subheader("Water Quality Results")
    safe = True
    if not (6.5 <= ph <= 8.5):
        st.error("❌ Unsafe pH level")
        safe = False
    if tds > 500:
        st.error("❌ High TDS level")
        safe = False
    if hardness > 300:
        st.error("❌ High Hardness level")
        safe = False
    if nitrate > 45:
        st.error("❌ High Nitrate level")
        safe = False

    if safe:
        st.success("✅ Water is safe for consumption")
    else:
        st.warning("⚠️ Water is contaminated")

    # Safety Gauge Moved Here
    st.subheader("Safety Gauge")
    score = 100
    if not (6.5 <= ph <= 8.5):
        score -= 25
    if tds > 500:
        score -= 25
    if hardness > 300:
        score -= 25
    if nitrate > 45:
        score -= 25

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Water Safety Index"},
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': "lime"},
               'steps': [
                   {'range': [0, 50], 'color': "red"},
                   {'range': [50, 75], 'color': "yellow"},
                   {'range': [75, 100], 'color': "green"}]}))
    st.plotly_chart(fig, use_container_width=True)

# -------- TAB 2: Data Overview --------
with tab2:
    st.subheader("Current Input Values")
    st.write(f"pH: {ph}")
    st.write(f"TDS: {tds} mg/L")
    st.write(f"Hardness: {hardness} mg/L")
    st.write(f"Nitrate: {nitrate} mg/L")

# -------- TAB 3: Awareness --------
with tab3:
    st.subheader("Awareness Info")
    st.write("""
    ☢️ Radioactive water contamination is extremely dangerous.  
    - Safe pH: 6.5 – 8.5  
    - TDS should be < 500 mg/L  
    - Hardness should be < 300 mg/L  
    - Nitrate should be < 45 mg/L  

    Always treat and test your water before consumption! 🚰
    """)
