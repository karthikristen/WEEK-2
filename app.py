import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Radioactive Water Contamination Detector", layout="wide")

# ================= BACKGROUND ELEMENTS =================
drops_html = ""
for i in range(12):
    delay = round(random.uniform(0, 6), 2)
    duration = round(random.uniform(5, 9), 2)
    left = random.randint(2, 95)
    size = random.randint(10, 20)
    drops_html += f"<div class='bg-drop' style='left:{left}%; font-size:{size}px; animation-delay:{delay}s; animation-duration:{duration}s;'>💧</div>"

rad_html = ""
for i in range(6):
    delay = round(random.uniform(0, 6), 2)
    duration = round(random.uniform(6, 12), 2)
    left = random.randint(5, 90)
    top = random.randint(5, 80)
    size = random.randint(18, 30)
    rad_html += f"<div class='bg-radio' style='left:{left}%; top:{top}%; font-size:{size}px; animation-delay:{delay}s; animation-duration:{duration}s;'>☢️</div>"

hazard_html = "<div class='hazard-bar'></div>"

# ================= CUSTOM CSS =================
css_block = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

/* General App Styling */
html, body, [class*="css"] {
  font-family: 'Bebas Neue', cursive;
  background-color: #0a0a0a;
  color: #e8f5e9;
  min-height: 100vh;
}

/* Ensure content stays on top */
.block-container, .main {
  position: relative;
  z-index: 2;
}

/* Title & Subtitle */
h1.app-title {
  text-align: center;
  color: #39FF14;
  font-size: 52px;
  margin-bottom: 4px;
  text-shadow: 0 0 10px #39FF14, 0 0 28px #FFD300;
}
p.app-sub {
  text-align: center;
  color: #FFD300;
  margin-top: 0;
  font-size: 20px;
  text-shadow: 0 0 10px #FFD300;
}

/* Tabs */
.stTabs [role="tablist"] button {
    background: #101010 !important;
    color: #39FF14 !important;
    border-radius: 12px !important;
    border: 1px solid rgba(57,255,20,0.3) !important;
    margin-right: 6px !important;
    padding: 8px 14px !important;
    transition: all .18s ease;
    font-size: 16px !important;
}
.stTabs [role="tablist"] button:hover {
    background: #39FF14 !important;
    color: black !important;
    transform: translateY(-2px) scale(1.03);
    box-shadow: 0 0 18px rgba(57,255,20,0.15);
}
.stTabs [role="tablist"] button[aria-selected="true"] {
    background: linear-gradient(90deg, #FFD300, #FF7518) !important;
    color: black !important;
    border: 1px solid #FFD300 !important;
    box-shadow: 0 0 26px rgba(255,211,0,0.35);
}

/* Results Glow */
.glow-green {
    color: #39FF14;
    text-shadow: 0 0 20px #39FF14;
    font-size: 22px;
}
.glow-red {
    color: red;
    text-shadow: 0 0 20px red;
    font-size: 22px;
}

/* Background Overlay */
.bg-overlay {
  position: fixed;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  overflow: hidden;
}
@keyframes dropFall {
  0%   { transform: translateY(-120px); opacity: 1; }
  100% { transform: translateY(110vh); opacity: 0; }
}
.bg-drop {
  position: absolute;
  top: -120px;
  color: #39FF14;
  text-shadow: 0 0 10px rgba(57,255,20,0.8), 0 0 20px rgba(255,211,0,0.06);
  animation-name: dropFall;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
  opacity: 0.95;
}
@keyframes radFloat {
  0%   { transform: translateY(0px) rotate(0deg);   opacity: .75; }
  50%  { transform: translateY(16px) rotate(180deg); opacity: 1; }
  100% { transform: translateY(0px) rotate(360deg);  opacity: .75; }
}
.bg-radio {
  position: absolute;
  color: #FFD300;
  text-shadow: 0 0 12px #FF7518, 0 0 24px #FF3131;
  animation-name: radFloat;
  animation-iteration-count: infinite;
  animation-timing-function: ease-in-out;
  opacity: 0.95;
}
.hazard-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 26px;
  background: repeating-linear-gradient(
    -45deg,
    #FFD300,
    #FFD300 20px,
    #000000 20px,
    #000000 40px
  );
  z-index: 1;
  opacity: 0.22;
  pointer-events: none;
}
</style>
"""

overlay_html = f"""
<div class="bg-overlay">
  {drops_html}
  {rad_html}
  {hazard_html}
</div>
"""

st.markdown(css_block + overlay_html, unsafe_allow_html=True)

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
    st.image("https://images.unsplash.com/photo-1505761671935-60b3a7427bad", caption="WHO Safe Drinking Water Limits")
    st.write("""
    - ✅ pH: 6.5 – 8.5  
    - ✅ TDS: < 500 mg/L  
    - ✅ Hardness: < 200 mg/L  
    - ✅ Nitrate: < 45 mg/L  
    """)

# ---- TAB 3 ----
with tabs[2]:
    st.subheader("⚠️ Dangers of Radioactive Water")
    st.image("https://images.unsplash.com/photo-1605733160314-4d4d92c9c3f1", caption="Radioactive Waste Warning")
    st.write("""
    - ☢️ Radioactive water exposure can cause **cancer, organ damage, and genetic mutations**.  
    - ☠️ Animals and plants also suffer from **biological accumulation** of radioactive isotopes.  
    - 💧 Continuous monitoring is **critical** for human survival.  
    """)

st.markdown("---")
st.markdown('<p style="text-align:center; color:#39FF14;">👨‍💻 Developed by Karthikeyan</p>', unsafe_allow_html=True)
