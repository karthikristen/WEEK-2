import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Radioactive Water Contamination Detector", layout="wide")

# ================= CUSTOM CSS =================
css_block = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

/* General Styling */
html, body, [class*="css"] {
  font-family: 'Bebas Neue', sans-serif;
  background-color: #0a0a0a;
  color: #FFD300;
  min-height: 100vh;
}

/* Title */
h1.app-title {
  text-align: center;
  color: #FFD300;
  font-size: 54px;
  margin-bottom: 2px;
  text-shadow: 0 0 12px #FFD300, 0 0 28px #FF7518;
}

/* Subtitle */
p.app-sub {
  text-align: center;
  color: #39FF14;
  margin-top: 0;
  font-size: 22px;
  text-shadow: 0 0 12px #39FF14, 0 0 22px #39FF14;
}

/* Tabs */
.stTabs [role="tablist"] button {
    background: #101010 !important;
    color: #FFD300 !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,211,0,0.4) !important;
    margin-right: 6px !important;
    padding: 8px 14px !important;
    transition: all .2s ease;
    font-size: 18px !important;
    text-shadow: 0 0 10px #FFD300;
}
.stTabs [role="tablist"] button:hover {
    background: #FFD300 !important;
    color: black !important;
    transform: translateY(-2px) scale(1.03);
    box-shadow: 0 0 20px rgba(255,211,0,0.3);
}
.stTabs [role="tablist"] button[aria-selected="true"] {
    background: linear-gradient(90deg, #FFD300, #FF7518) !important;
    color: black !important;
    border: 1px solid #FFD300 !important;
    box-shadow: 0 0 24px rgba(255,211,0,0.4);
}

/* Results Glow */
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

/* Images */
.stImage img {
    border-radius: 12px;
    box-shadow: 0 0 20px rgba(255,211,0,0.2);
    margin-bottom: 16px;
}

/* Footer */
.footer {
    text-align: center;
    color: #FFD300;
    margin-top: 30px;
    font-size: 18px;
    text-shadow: 0 0 10px #FFD300, 0 0 20px #FF7518;
}
</style>
"""
st.markdown(css_block, unsafe_allow_html=True)

# ================= FUNCTIONS =================
def predict_contamination(ph, tds, hardness, nitrate):
    score = 0
    if ph < 6.5 or ph > 8.5: score += 30
    if tds > 500: score += 25
    if hardness > 200: score += 20
    if nitrate > 45: score += 25
    return score

def show_risk_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "☢️ Risk Level (%)", 'font': {'color': '#FFD300', 'size': 20}},
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
    st.plotly_chart(fig, use_container_width=True)

# ================= UI =================
st.markdown("<h1 class='app-title'>💧☢️ Radioactive Water Contamination Detector</h1>", unsafe_allow_html=True)
st.markdown("<p class='app-sub'>Futuristic AI/ML Powered System | Developed by Karthikeyan</p>", unsafe_allow_html=True)

tabs = st.tabs(["🔬 Contamination Check", "📊 Safety Meter", "⚠️ Radioactive Awareness"])

# ---- TAB 1 ----
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

        # Save dataset
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

# ---- TAB 2 ----
with tabs[1]:
    st.subheader("📊 Safe vs Unsafe Water Levels")
    st.image("safety.png", caption="WHO Safe Drinking Water Limits")  # replace with your own
    st.write("""
    - ✅ pH: 6.5 – 8.5  
    - ✅ TDS: < 500 mg/L  
    - ✅ Hardness: < 200 mg/L  
    - ✅ Nitrate: < 45 mg/L  
    """)

# ---- TAB 3 ----
with tabs[2]:
    st.subheader("⚠️ Dangers of Radioactive Water")
    st.image("danger.png", caption="Radioactive Waste Warning")  # replace with your own
    st.write("""
    - ☢️ Radioactive water exposure can cause **cancer, organ damage, and genetic mutations**.  
    - ☠️ Animals and plants also suffer from **biological accumulation** of radioactive isotopes.  
    - 💧 Continuous monitoring is **critical** for human survival.  
    """)

# ---- FOOTER ----
st.markdown('<p class="footer">👨‍💻 Developed by Karthikeyan</p>', unsafe_allow_html=True)
