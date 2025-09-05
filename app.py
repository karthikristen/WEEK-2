# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random
from io import StringIO

st.set_page_config(page_title="Radioactive Water Detector", layout="wide")

# =========================
# THEME & BACKGROUND (CSS)
# =========================
# Generate background elements once (drops + radio symbols)
NUM_DROPS = 24
NUM_RADIOS = 6

drops = []
for _ in range(NUM_DROPS):
    left = random.randint(0, 98)        # % from left
    dur = round(random.uniform(3.5, 7.5), 2)   # seconds
    delay = round(random.uniform(0, 5), 2)     # seconds
    size = random.randint(18, 26)       # px font size
    drops.append(
        f"<div class='drop' style='left:{left}%;"
        f"animation-duration:{dur}s; animation-delay:{delay}s; font-size:{size}px;'>💧</div>"
    )

radios = []
for _ in range(NUM_RADIOS):
    left = random.randint(6, 92)
    top = random.randint(12, 78)
    delay = round(random.uniform(0, 4), 2)
    size = random.randint(32, 56)
    radios.append(
        f"<div class='radio' style='left:{left}%; top:{top}%;"
        f"animation-delay:{delay}s; font-size:{size}px;'>☢️</div>"
    )

hazard_bar = "<div class='hazard-bar'></div>"

background_html = "".join(drops) + "".join(radios) + hazard_bar

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

/* Base app surface */
.stApp {{
  background-color: #0a0a0a;            /* Steel Black */
  position: relative;
  min-height: 100vh;
  overflow-x: hidden;                   /* prevent sideways scroll only */
  font-family: 'Bebas Neue', sans-serif !important;
}}
/* Ensure content stays above background elements */
.block-container {{
  position: relative;
  z-index: 1;
}}

/* Header styles */
h1.title {{
  text-align: center;
  color: #39FF14;
  font-size: 58px;
  line-height: 1.05;
  letter-spacing: 1px;
  text-shadow: 0 0 10px #39FF14, 0 0 24px #39FF14, 0 0 40px #FFD300;
  margin: 18px 0 8px 0;
  animation: titlePulse 3s ease-in-out infinite;
}}
@keyframes titlePulse {{
  0% {{ text-shadow: 0 0 10px #39FF14, 0 0 24px #39FF14; }}
  50% {{ text-shadow: 0 0 18px #FFD300, 0 0 38px #FF7518; }}
  100% {{ text-shadow: 0 0 10px #39FF14, 0 0 24px #39FF14; }}
}}

p.subtitle {{
  text-align: center;
  color: #FFD300;
  font-size: 22px;
  margin: 0 0 22px 0;
  text-shadow: 0 0 10px #FFD300, 0 0 18px #39FF14;
  animation: subPulse 2.4s ease-in-out infinite;
}}
@keyframes subPulse {{
  0% {{ opacity: .75; }}
  50% {{ opacity: 1; }}
  100% {{ opacity: .75; }}
}}

/* Tabs as glowing hazard buttons */
.stTabs [role="tablist"] button[role="tab"] {{
  background: #121212 !important;
  color: #39FF14 !important;
  border-radius: 12px !important;
  border: 2px solid #FFD300 !important;
  margin-right: 8px !important;
  font-size: 18px !important;
  text-shadow: 0 0 10px #39FF14;
  transition: all .25s ease;
}}
.stTabs [role="tablist"] button[aria-selected="true"] {{
  background: #1b1b1b !important;
  box-shadow: 0 0 18px rgba(255,211,0,.35);
}}
.stTabs [role="tablist"] button:hover {{
  transform: translateY(-1px) scale(1.03);
}}

/* Inputs in glowing cards */
div[data-testid="stNumberInput"] > label, div[data-testid="stTextInput"] > label {{
  color: #39FF14 !important;
  font-size: 18px !important;
}}
div[data-testid="stNumberInput"] input, div[data-testid="stTextInput"] input {{
  background: #1a1a1a !important;
  color: #f0f0f0 !important;
  border: 2px solid #39FF14 !important;
  border-radius: 12px !important;
  box-shadow: 0 0 12px rgba(57,255,20,.25) inset;
}}
/* Nice container around inputs */
.form-card {{
  background: linear-gradient(180deg, rgba(26,26,26,.95), rgba(10,10,10,.95));
  border: 1px solid rgba(57,255,20,.35);
  border-radius: 16px;
  box-shadow: 0 0 24px rgba(57,255,20,.25);
  padding: 18px 18px 6px 18px;
  margin: 10px 0 20px 0;
}}

/* Gauge container spacing */
.gauge-wrap {{
  margin-top: 14px;
}}

/* Background: falling drops */
@keyframes fall {{
  0%   {{ transform: translateY(-100px); opacity: 1; }}
  100% {{ transform: translateY(110vh);  opacity: 0; }}
}}
.drop {{
  position: fixed;
  top: -60px;
  color: #00e6e6;
  text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
  animation-name: fall;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
  z-index: 0;
  pointer-events: none;
}}

/* Background: floating/rotating radioactive symbols */
@keyframes floatRotate {{
  0%   {{ transform: translateY(0) rotate(0deg);   opacity: .75; }}
  50%  {{ transform: translateY(18px) rotate(180deg); opacity: 1; }}
  100% {{ transform: translateY(0) rotate(360deg);  opacity: .75; }}
}}
.radio {{
  position: fixed;
  color: #39FF14;
  text-shadow: 0 0 12px #39FF14, 0 0 26px #39FF14;
  animation: floatRotate 8s ease-in-out infinite;
  z-index: 0;
  pointer-events: none;
}}

/* Animated hazard stripe at bottom (subtle, behind content) */
.hazard-bar {{
  position: fixed;
  bottom: 0; left: 0; width: 100%; height: 22px;
  background: repeating-linear-gradient(
    -45deg,
    #FFD300, #FFD300 18px,
    #000000 18px, #000000 36px
  );
  animation: slide 6s linear infinite;
  z-index: 0;
  opacity: .35;
  pointer-events: none;
}}
@keyframes slide {{
  0%   {{ background-position: 0 0; }}
  100% {{ background-position: 120px 0; }}
}}
</style>

<!-- Background elements -->
{background_html}
""", unsafe_allow_html=True)

# =========================
# LOGIC
# =========================
def predict_contamination(ph: float, tds: float, hardness: float, nitrate: float) -> int:
    """Simple threshold score. 0–100."""
    score = 0
    if ph < 6.5 or ph > 8.5: score += 30
    if tds > 500:            score += 25
    if hardness > 200:       score += 20
    if nitrate > 45:         score += 25
    return min(score, 100)

def show_risk_gauge(score: int) -> None:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={'suffix': "%"},
        title={'text': "Radioactive Risk"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar':  {'color': "#FF3131" if score >= 60 else "#FF7518" if score >= 30 else "#39FF14"},
            'steps': [
                {'range': [0, 30],  'color': "rgba(57,255,20,0.25)"},
                {'range': [30, 60], 'color': "rgba(255,211,0,0.25)"},
                {'range': [60, 100],'color': "rgba(255,49,49,0.25)"}
            ],
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

# =========================
# UI
# =========================
st.markdown("<h1 class='title'>💧 ☢️  Radioactive Water Contamination Detector</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Futuristic AI/ML Powered System  |  Developed by Karthikeyan</p>", unsafe_allow_html=True)

tabs = st.tabs(["🔬 Contamination Check", "📊 Safety Meter", "⚠️ Radioactive Awareness"])

# ---- TAB 1: Check ----
with tabs[0]:
    st.markdown("<h3 style='text-align:center;color:#39FF14;'>🔍 Enter Water Parameters</h3>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='form-card'>", unsafe_allow_html=True)
        cols = st.columns(2)
        with cols[0]:
            ph = st.number_input("pH Level", min_value=0.0, max_value=14.0, value=7.0, step=0.01)
            hardness = st.number_input("Hardness (mg/L)", min_value=0.0, max_value=1000.0, value=150.0, step=1.0)
        with cols[1]:
            tds = st.number_input("TDS (mg/L)", min_value=0.0, max_value=2000.0, value=300.0, step=1.0)
            nitrate = st.number_input("Nitrate (mg/L)", min_value=0.0, max_value=500.0, value=20.0, step=1.0)

        location = st.text_input("📍 Location", value="")
        run = st.button("Run Analysis", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if run:
        score = predict_contamination(ph, tds, hardness, nitrate)

        if score < 30:
            msg = '<p style="color:#39FF14; text-shadow:0 0 14px #39FF14;">✅ Safe: No significant radioactive contamination detected.</p>'
        elif score < 60:
            msg = '<p style="color:#FFD300; text-shadow:0 0 14px #FFD300;">⚠️ Moderate Risk: Some radioactive traces possible.</p>'
        else:
            msg = '<p style="color:#FF3131; text-shadow:0 0 16px #FF3131;">☢️ High Risk: Potential radioactive contamination detected!</p>'

        st.markdown(msg, unsafe_allow_html=True)
        st.markdown("<div class='gauge-wrap'>", unsafe_allow_html=True)
        show_risk_gauge(score)
        st.markdown("</div>", unsafe_allow_html=True)

        # Save new row and offer download (no crash if file missing)
        new_row = pd.DataFrame(
            [[location, ph, tds, hardness, nitrate, score]],
            columns=["Location", "pH", "TDS", "Hardness", "Nitrate", "RiskScore"]
        )
        try:
            old = pd.read_csv("water_data.csv")
            df = pd.concat([old, new_row], ignore_index=True)
        except Exception:
            df = new_row
        df.to_csv("water_data.csv", index=False)

        st.success("Data saved successfully ✅")
        csv_buf = StringIO()
        df.to_csv(csv_buf, index=False)
        st.download_button(
            "📥 Download Dataset",
            data=csv_buf.getvalue(),
            file_name="water_data.csv",
            mime="text/csv",
            use_container_width=True
        )

# ---- TAB 2: Safety Meter ----
with tabs[1]:
    st.markdown("<h3 style='text-align:center;color:#39FF14;'>📊 Safe vs Unsafe Water Levels</h3>", unsafe_allow_html=True)
    st.markdown("""
<div style="display:flex; justify-content:center;">
  <div style="text-align:left; color:#e8e8e8; font-size:20px; line-height:1.6;">
    ✅ <b>pH</b>: 6.5 – 8.5<br/>
    ✅ <b>TDS</b>: &lt; 500 mg/L<br/>
    ✅ <b>Hardness</b>: &lt; 200 mg/L<br/>
    ✅ <b>Nitrate</b>: &lt; 45 mg/L
  </div>
</div>
""", unsafe_allow_html=True)

# ---- TAB 3: Awareness ----
with tabs[2]:
    st.markdown("<h3 style='text-align:center;color:#39FF14;'>⚠️ Dangers of Radioactive Water</h3>", unsafe_allow_html=True)
    st.markdown("""
- ☢️ Long-term exposure may increase risks of **cancer**, **organ damage**, and **genetic mutations**.
- ☠️ Wildlife and plants can suffer from **bioaccumulation** of radioactive isotopes.
- 💧 Continuous monitoring and prompt treatment/filtration are **critical**.
""")
    
st.markdown("<hr/>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#39FF14;'>👨‍💻 Developed by Karthikeyan</p>", unsafe_allow_html=True)
