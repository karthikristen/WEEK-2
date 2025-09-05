import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ------------------- CUSTOM CSS -------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

    body, .stApp {
        background-color: OliveDrab !important;
        color: #39FF14;
        font-family: 'Bebas Neue', cursive !important;
    }

    h1, h2, h3, h4, h5, h6, p, div, button {
        font-family: 'Bebas Neue', cursive !important;
        text-align: center !important;
    }

    .stTabs [role="tablist"] button {
        background: #111 !important;
        color: #39FF14 !important;
        border-radius: 10px;
        border: 1px solid #39FF14;
        margin-right: 5px;
        transition: all 0.3s ease-in-out;
    }
    .stTabs [role="tablist"] button:hover {
        background: #39FF14 !important;
        color: black !important;
        transform: scale(1.05);
    }

    .glow-green {
        color: #39FF14;
        text-shadow: 0 0 20px #39FF14;
        font-size: 24px;
    }
    .glow-red {
        color: red;
        text-shadow: 0 0 20px red;
        font-size: 24px;
    }

    /* Droplet background container */
    .drop-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        z-index: -1;
    }

    .water-drop {
        position: absolute;
        top: -10px;
        width: 6px;
        height: 18px;
        background: #39FF14;
        border-radius: 50%;
        animation: drop 4s linear infinite;
    }

    @keyframes drop {
        0% { top: -20px; opacity: 0; }
        30% { opacity: 1; }
        100% { top: 100vh; opacity: 0; }
    }
    </style>
""", unsafe_allow_html=True)

# ------------------- WATER DROPS (NO EXTRA SPACE) -------------------
drop_html = "<div class='drop-container'>"
for i in range(20):  # number of drops
    drop_html += f"<div class='water-drop' style='left:{i*5}%; animation-delay:{i*0.5}s;'></div>"
drop_html += "</div>"
st.markdown(drop_html, unsafe_allow_html=True)

# ------------------- PREDICTION FUNCTION -------------------
def predict_contamination(ph, tds, hardness, nitrate):
    score = 0
    if ph < 6.5 or ph > 8.5: score += 30
    if tds > 500: score += 25
    if hardness > 200: score += 20
    if nitrate > 45: score += 25
    return score

# ------------------- GAUGE -------------------
def show_risk_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Radioactive Risk %"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "red" if score >= 60 else "orange" if score >= 30 else "green"},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 60], 'color': "yellow"},
                {'range': [60, 100], 'color': "red"}
            ],
        }
    ))
    st.plotly_chart(fig)

# ------------------- APP STRUCTURE -------------------
st.markdown('<h1 class="glow-green">💧☢️ Radioactive Water Contamination Detector</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="glow-green">Futuristic AI/ML Powered System | Developed by Karthikeyan</h3>', unsafe_allow_html=True)

tabs = st.tabs(["🔬 Contamination Check", "📊 Safety Meter", "⚠️ Radioactive Awareness"])

# ---- TAB 1: Check ----
with tabs[0]:
    st.subheader("🔍 Enter Water Parameters")

    ph = st.number_input("pH Level", 0.0, 14.0, 7.0)
    tds = st.number_input("TDS (mg/L)", 0.0, 2000.0, 300.0)
    hardness = st.number_input("Hardness (mg/L)", 0.0, 1000.0, 150.0)
    nitrate = st.number_input("Nitrate (mg/L)", 0.0, 500.0, 20.0)
    location = st.text_input("📍 Location")

    if st.button("Run Analysis"):
        score = predict_contamination(ph, tds, hardness, nitrate)

        if score < 30:
            result = '<p class="glow-green">✅ Safe: No significant radioactive contamination detected.</p>'
        elif score < 60:
            result = '<p class="glow-red">⚠️ Moderate Risk: Some radioactive traces possible.</p>'
        else:
            result = '<p class="glow-red">☢️ High Risk: Potential radioactive contamination detected!</p>'

        st.markdown(result, unsafe_allow_html=True)
        show_risk_gauge(score)

        # Save to dataset
        new_data = pd.DataFrame([[location, ph, tds, hardness, nitrate, score]],
                                columns=["Location", "pH", "TDS", "Hardness", "Nitrate", "RiskScore"])
        try:
            old_data = pd.read_csv("water_data.csv")
            df = pd.concat([old_data, new_data], ignore_index=True)
        except:
            df = new_data
        df.to_csv("water_data.csv", index=False)

        st.success("Data saved successfully ✅")
        st.download_button("📥 Download Dataset", data=df.to_csv(index=False),
                           file_name="water_data.csv", mime="text/csv")

# ---- TAB 2: Safety Meter ----
with tabs[1]:
    st.subheader("📊 Safe vs Unsafe Water Levels")
    st.image("https://i.imgur.com/EVqH2YV.png", caption="WHO Safe Drinking Water Limits")
    st.write("""
    - ✅ pH: 6.5 – 8.5  
    - ✅ TDS: < 500 mg/L  
    - ✅ Hardness: < 200 mg/L  
    - ✅ Nitrate: < 45 mg/L  
    """)

# ---- TAB 3: Awareness ----
with tabs[2]:
    st.subheader("⚠️ Dangers of Radioactive Water")
    st.image("https://i.imgur.com/whs7YdF.png", caption="Radioactive Waste Warning")
    st.write("""
    - ☢️ Radioactive water exposure can cause **cancer, organ damage, and genetic mutations**.  
    - ☠️ Animals and plants also suffer from **biological accumulation** of radioactive isotopes.  
    - 💧 Continuous monitoring is **critical** for human survival.  
    """)

st.markdown("---")
st.markdown('<p style="text-align:center; color:#39FF14;">👨‍💻 Developed by Karthikeyan</p>', unsafe_allow_html=True)
