import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ------------------- CUSTOM CSS -------------------
st.markdown("""
    <style>
    body {
        background-color: black;
        color: #FFFF33;
        font-family: monospace;
    }
    .stTabs [role="tablist"] button {
        background: #111 !important;
        color: #FFFF33 !important;
        border-radius: 10px;
        border: 1px solid #FFFF33;
        margin-right: 5px;
        transition: all 0.3s ease-in-out;
        text-shadow: 0 0 10px #FFFF33, 0 0 20px #FFFF33;
    }
    .stTabs [role="tablist"] button:hover {
        background: #FFFF33 !important;
        color: black !important;
        transform: scale(1.05);
        text-shadow: 0 0 20px #FFFF33, 0 0 30px #FFFF33;
    }
    .glow-yellow {
        color: #FFFF33 !important;
        text-shadow: 0 0 10px #FFFF33, 0 0 20px #FFFF33, 0 0 40px #FFFF33;
        font-size: 22px;
    }
    h1, h2, h3, .stMarkdown, .stText, .stCaption {
        color: #FFFF33 !important;
        text-shadow: 0 0 10px #FFFF33, 0 0 20px #FFFF33, 0 0 40px #FFFF33;
    }
    </style>
""", unsafe_allow_html=True)

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
        title={'text': "☢️ Radioactive Risk %", 'font': {'color': '#FFFF33'}},
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
st.title("💧☢️ Radioactive Water Contamination Detector")
st.caption('<p class="glow-yellow">Futuristic AI/ML Powered System | Developed by Karthikeyan</p>', unsafe_allow_html=True)

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
            result = '<p class="glow-yellow">✅ Safe: No significant radioactive contamination detected.</p>'
        elif score < 60:
            result = '<p class="glow-yellow">⚠️ Moderate Risk: Some radioactive traces possible.</p>'
        else:
            result = '<p class="glow-yellow">☢️ High Risk: Potential radioactive contamination detected!</p>'

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
    st.image("https://images.unsplash.com/photo-1528825871115-3581a5387919", caption="WHO Safe Drinking Water Limits")
    st.write("""
    - ✅ pH: 6.5 – 8.5  
    - ✅ TDS: < 500 mg/L  
    - ✅ Hardness: < 200 mg/L  
    - ✅ Nitrate: < 45 mg/L  
    """)

# ---- TAB 3: Awareness ----
with tabs[2]:
    st.subheader("⚠️ Dangers of Radioactive Water")
    st.image("https://images.unsplash.com/photo-1600644356991-c3e3d1a73f4b", caption="Radioactive Waste Warning")
    st.write("""
    - ☢️ Radioactive water exposure can cause **cancer, organ damage, and genetic mutations**.  
    - ☠️ Animals and plants also suffer from **biological accumulation** of radioactive isotopes.  
    - 💧 Continuous monitoring is **critical** for human survival.  
    """)

st.markdown("---")
st.markdown('<p style="text-align:center;" class="glow-yellow">👨‍💻 Developed by Karthikeyan</p>', unsafe_allow_html=True)
