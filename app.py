# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random
from io import StringIO

st.set_page_config(page_title="Radioactive Water Contamination Detector", layout="wide")

# ---------------- CSS + BACKGROUND OVERLAY (single injection) ----------------
NUM_DROPS = 26
NUM_RADIOS = 5

# Build HTML for drops and radios (randomized positions/speeds)
drops_html = ""
for i in range(NUM_DROPS):
    left = random.randint(0, 98)
    dur = round(random.uniform(3.5, 8.0), 2)
    delay = round(random.uniform(0, 5), 2)
    size = random.randint(12, 26)
    drops_html += (
        f"<div class='bg-drop' style='left:{left}%; font-size:{size}px; "
        f"animation-duration:{dur}s; animation-delay:{delay}s;'>💧</div>"
    )

rad_html = ""
for i in range(NUM_RADIOS):
    left = random.randint(4, 92)
    top = random.randint(8, 78)
    delay = round(random.uniform(0, 3), 2)
    sz = random.randint(28, 64)
    rad_html += (
        f"<div class='bg-radio' style='left:{left}%; top:{top}%; "
        f"animation-delay:{delay}s; font-size:{sz}px;'>☢️</div>"
    )

hazard_html = "<div class='hazard-bar'></div>"

# Single CSS + HTML block
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

/* App surface */
[data-testid="stAppViewContainer"], .stApp {{
  background-color: #0a0a0a; /* steel black base */
  color: #e8f5e9;
  font-family: 'Bebas Neue', sans-serif;
  min-height: 100vh;
}}

/* Ensure Streamlit content sits above the overlay */
.block-container, .main {{
  position: relative;
  z-index: 2; /* foreground */
}}

/* Title & subtitle */
h1.app-title {{
  text-align: center;
  color: #39FF14;
  font-size: 52px;
  margin-bottom: 4px;
  text-shadow: 0 0 10px #39FF14, 0 0 28px #FFD300;
}}
p.app-sub {{
  text-align: center;
  color: #FFD300;
  margin-top: 0;
  font-size: 20px;
  text-shadow: 0 0 10px #FFD300;
}

/* Tabs: base + hover + active highlight */
.stTabs [role="tablist"] button {{
    background: #101010 !important;
    color: #39FF14 !important;
    border-radius: 12px !important;
    border: 1px solid rgba(57,255,20,0.3) !important;
    margin-right: 6px !important;
    padding: 8px 14px !important;
    transition: all .18s ease;
    font-size: 16px !important;
}}
.stTabs [role="tablist"] button:hover {{
    background: #39FF14 !important;
    color: black !important;
    transform: translateY(-2px) scale(1.03);
    box-shadow: 0 0 18px rgba(57,255,20,0.15);
}}
/* active/selected */
.stTabs [role="tablist"] button[aria-selected="true"] {{
    background: linear-gradient(90deg, #FFD300, #FF7518) !important;
    color: black !important;
    border: 1px solid #FFD300 !important;
    box-shadow: 0 0 26px rgba(255,211,0,0.35);
}}

/* center input card */
.form-card {{
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
  padding: 16px;
  border-radius: 12px;
  background: linear-gradient(180deg, rgba(15,15,15,0.88), rgba(6,6,6,0.82));
  border: 1px solid rgba(57,255,20,0.08);
  box-shadow: 0 8px 30px rgba(0,0,0,0.6), inset 0 0 8px rgba(57,255,20,0.02);
}

/* labels & inputs */
div[data-testid="stNumberInput"] > label, div[data-testid="stTextInput"] > label {{
    color: #39FF14 !important;
}}
div[data-testid="stNumberInput"] input, div[data-testid="stTextInput"] input {{
    background: #121212 !important;
    color: #f4f4f4 !important;
    border: 2px solid rgba(57,255,20,0.25) !important;
    border-radius: 10px !important;
}}

/* gauge wrap */
.gauge-wrap {{
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}}

/* ------------------ BACKGROUND OVERLAY (behind content) ------------------ */
.bg-overlay {{
  position: fixed;
  inset: 0; /* top:0; left:0; right:0; bottom:0 */
  z-index: 1; /* behind .block-container which is z-index:2 */
  pointer-events: none;
  overflow: hidden;
}}

/* falling drops inside overlay */
@keyframes dropFall {{
  0% {{ transform: translateY(-120px); opacity: 1; }}
  100% {{ transform: translateY(110vh); opacity: 0; }}
}}
.bg-drop {{
  position: absolute;
  top: -120px;
  color: #39FF14;
  text-shadow: 0 0 10px rgba(57,255,20,0.8), 0 0 20px rgba(255,211,0,0.06);
  animation-name: dropFall;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
  opacity: 0.95;
}

/* rotating/pulsing radioactive signs */
@keyframes radFloat {{
  0%   {{ transform: translateY(0px) rotate(0deg);   opacity: .75; }}
  50%  {{ transform: translateY(16px) rotate(180deg); opacity: 1; }}
  100% {{ transform: translateY(0px) rotate(360deg);  opacity: .75; }}
}}
.bg-radio {{
  position: absolute;
  color: #FFD300;
  text-shadow: 0 0 12px #FF7518, 0 0 24px #FF3131;
  animation-name: radFloat;
  animation-duration: 8s;
  animation-iteration-count: infinite;
  animation-timing-function: ease-in-out;
  opacity: 0.95;
}

/* hazard stripe bottom */
.hazard-bar {{
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

<!-- Overlay HTML: drops + radios + hazard -->
<div class="bg-overlay">
  {drops_html}
  {rad_html}
  {hazard_html}
</div>
""", unsafe_allow_html=True)

# ---------------- App Content ----------------
st.markdown('<h1 class="app-title title">💧☢️ Radioactive Water Contamination Detector</h1>', unsafe_allow_html=True)
st.markdown('<p class="app-sub subtitle">Futuristic AI/ML Powered System  |  Developed by <b>Karthikeyan</b></p>', unsafe_allow_html=True)

# Tabs
tabs = st.tabs(["🔬 Contamination Check", "📊 Safety Meter", "⚠️ Radioactive Awareness"])

# ---------------- Prediction function + gauge ----------------
def predict_contamination(ph, tds, hardness, nitrate):
    score = 0
    if ph < 6.5 or ph > 8.5:
        score += 30
    if tds > 500:
        score += 25
    if hardness > 200:
        score += 20
    if nitrate > 45:
        score += 25
    return min(score, 100)

def show_risk_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={'suffix': "%"},
        title={'text': "Radioactive Risk"},
        gauge={
            'axis': {'range': [0,100]},
            'bar': {'color': "#FF3131" if score>=60 else "#FF7518" if score>=30 else "#39FF14"},
            'steps': [
                {'range':[0,30], 'color': "rgba(57,255,20,0.18)"},
                {'range':[30,60], 'color': "rgba(255,211,0,0.18)"},
                {'range':[60,100], 'color': "rgba(255,49,49,0.18)"}
            ],
        }
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

# ------------------ TAB 1: Contamination Check (with Safety Meter below) ------------------
with tabs[0]:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)

    st.subheader("🔍 Enter Water Parameters")
    cols = st.columns(2)
    with cols[0]:
        ph = st.number_input("pH Level", min_value=0.0, max_value=14.0, value=7.0, step=0.1)
        tds = st.number_input("TDS (mg/L)", min_value=0.0, max_value=2000.0, value=300.0, step=1.0)
    with cols[1]:
        hardness = st.number_input("Hardness (mg/L)", min_value=0.0, max_value=1000.0, value=150.0, step=1.0)
        nitrate = st.number_input("Nitrate (mg/L)", min_value=0.0, max_value=500.0, value=20.0, step=1.0)

    location = st.text_input("📍 Location (optional)")
    run = st.button("Run Analysis")
    st.markdown('</div>', unsafe_allow_html=True)

    if run:
        score = predict_contamination(ph, tds, hardness, nitrate)

        if score < 30:
            st.markdown('<p style="color:#39FF14; text-shadow:0 0 12px #39FF14;">✅ Safe: No significant radioactive contamination detected.</p>', unsafe_allow_html=True)
        elif score < 60:
            st.markdown('<p style="color:#FFD300; text-shadow:0 0 12px #FFD300;">⚠️ Moderate Risk: Some radioactive traces possible.</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#FF3131; text-shadow:0 0 16px #FF3131;">☢️ High Risk: Potential radioactive contamination detected!</p>', unsafe_allow_html=True)

        st.markdown('<div class="gauge-wrap">', unsafe_allow_html=True)
        show_risk_gauge(score)
        st.markdown('</div>', unsafe_allow_html=True)

        # Save to CSV and provide download
        new_row = pd.DataFrame([[location, ph, tds, hardness, nitrate, score]],
                               columns=["Location","pH","TDS","Hardness","Nitrate","RiskScore"])
        try:
            old = pd.read_csv("water_data.csv")
            df = pd.concat([old, new_row], ignore_index=True)
        except Exception:
            df = new_row
        df.to_csv("water_data.csv", index=False)
        st.success("Data saved successfully ✅")
        csv_buf = StringIO()
        df.to_csv(csv_buf, index=False)
        st.download_button("📥 Download Dataset", data=csv_buf.getvalue(),
                           file_name="water_data.csv", mime="text/csv")

# ------------------ TAB 2: Safety Meter (visual explanation + SVG icon) ------------------
with tabs[1]:
    st.subheader("📊 Safe vs Unsafe Water Levels")
    # Inline copyright-free SVG (shield / check) — always available
    shield_svg = """
    <div style="display:flex; justify-content:center;">
      <svg width="220" height="160" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="g1" x1="0" x2="1">
            <stop offset="0" stop-color="#39FF14"/>
            <stop offset="1" stop-color="#FFD300"/>
          </linearGradient>
        </defs>
        <path d="M32 4 L56 12 L56 28 C56 44 44 58 32 60 C20 58 8 44 8 28 L8 12 Z" fill="url(#g1)" stroke="#222" stroke-width="0.8"/>
        <path d="M22 32 L28 38 L42 24" fill="none" stroke="#071" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
    """
    st.markdown(shield_svg, unsafe_allow_html=True)
    st.write("""
    - ✅ **pH:** 6.5 – 8.5  
    - ✅ **TDS:** < 500 mg/L  
    - ✅ **Hardness:** < 200 mg/L  
    - ✅ **Nitrate:** < 45 mg/L  
    """)

# ------------------ TAB 3: Awareness (warning SVG + explanation) ------------------
with tabs[2]:
    st.subheader("⚠️ Dangers of Radioactive Water")
    warning_svg = """
    <div style="display:flex; justify-content:center;">
      <svg width="200" height="140" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="gw" x1="0" x2="1">
            <stop offset="0" stop-color="#FFD300"/>
            <stop offset="1" stop-color="#FF7518"/>
          </linearGradient>
        </defs>
        <path d="M32 4 L60 56 H4 Z" fill="url(#gw)" stroke="#220" stroke-width="0.6"/>
        <circle cx="32" cy="40" r="6" fill="#0a0a0a"/>
        <text x="32" y="47" font-size="8" text-anchor="middle" fill="#FF3131" font-weight="bold">☢</text>
      </svg>
    </div>
    """
    st.markdown(warning_svg, unsafe_allow_html=True)
    st.write("""
    - ☢️ **Long-term exposure** increases risk of cancer, organ damage, and genetic effects.  
    - ☠️ **Bioaccumulation**: animals & plants can retain isotopes and pass them up the food chain.  
    - 💧 **Regular testing & filtration** are essential for safety.
    """)

# footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#39FF14;">👨‍💻 Developed by Karthikeyan</p>', unsafe_allow_html=True)
