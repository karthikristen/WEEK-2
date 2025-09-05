import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random

# ------------------- CUSTOM CSS -------------------
st.markdown("""
<style>
/* ----- IMPORT BEBAS NEUE ----- */
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

/* ----- BODY & OLIVE GREEN GRADIENT ----- */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #556B2F, #6B8E23, #808000, #556B2F);
    background-size: 400% 400%;
    animation: gradientBG 20s ease infinite;
}
@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ----- GLOWING TABS ----- */
.stTabs [role="tablist"] button {
    background: #3B5323 !important;
    color: #39FF14 !important;
    border-radius: 10px;
    border: 1px solid #39FF14;
    margin-right: 5px;
    transition: all 0.3s ease-in-out;
    font-family: 'Bebas Neue', cursive;
}
.stTabs [role="tablist"] button:hover,
.stTabs [role="tablist"] button:focus {
    background: #39FF14 !important;
    color: black !important;
    box-shadow: 0 0 20px #39FF14, 0 0 40px #39FF14;
    transform: scale(1.1);
}

/* ----- GLOWING HEADINGS & CENTERED ----- */
h1, h2, h3, h4, h5, h6, p {
    font-family: 'Bebas Neue', cursive;
    text-align: center;
}
.centered-glow {
    color: #39FF14;
    text-shadow: 0 0 10px #39FF14, 0 0 20px #39FF14;
}

/* ----- CENTER INPUTS AND BUTTONS ----- */
.stNumberInput, .stTextInput, .stButton button {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-left: auto;
    margin-right: auto;
    font-family: 'Bebas Neue', cursive;
}

/* ----- GLOWING BUTTONS ----- */
button {
    background: #3B5323 !important;
    color: #39FF14 !important;
    border: 1px solid #39FF14 !important;
    border-radius: 10px;
    transition: 0.3s all;
}
button:hover {
    background: #39FF14 !important;
    color: black !important;
    box-shadow: 0 0 20px #39FF14;
    transform: scale(1.1);
}

/* ----- FALLING DROPLETS ----- */
@keyframes drop {
    0% { top: -20px; opacity: 0; }
    30% { opacity: 1; }
    100% { top: 100vh; opacity: 0; }
}
.droplet {
    position: fixed;  /* moves with viewport, no extra space */
    width: 4px;
    height: 15px;
    background: #39FF14;
    border-radius: 50%;
    animation: drop linear infinite;
    z-index: -1;      /* behind all content */
}

/* ----- FLOATING RADIOACTIVE ICONS ----- */
@keyframes floatY {
    0% { transform: translateY(0px);}
    50% { transform: translateY(-15px);}
    100% { transform: translateY(0px);}
}
</style>
""", unsafe_allow_html=True)

# ------------------- DROPLETS -------------------
for i in range(50):
    left = random.randint(0, 95)
    delay = random.uniform(0, 5)
    duration = random.uniform(3, 8)
    width = random.randint(2, 6)
    height = random.randint(10, 20)
    st.markdown(f"""
    <div class="droplet" style="
        left:{left}%;
        width:{width}px;
        height:{height}px;
        animation-duration:{duration}s;
        animation-delay:{delay}s;
    "></div>
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
        mode="gauge+number+delta",
        value=score,
        number={'suffix': "%"},
        delta={'reference': 0, 'increasing': {'color': "red"}},
        title={'text': "Radioactive Risk"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "red" if score >= 60 else "yellow" if score >= 30 else "green"},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 60], 'color': "yellow"},
                {'range': [60, 100], 'color': "red"}
            ]
        }
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      font={'color': "#39FF14", 'family': "Bebas Neue"},
                      transition={'duration': 1000, 'easing': 'cubic-in-out'})
    st.plotly_chart(fig, use_container_width=True)

# ------------------- RISK MESSAGE -------------------
def show_risk_message(score):
    if score < 30:
        st.markdown('<p class="centered-glow">✅ Safe: No significant radioactive contamination detected.</p>', unsafe_allow_html=True)
    elif score < 60:
        st.markdown('<p class="centered-glow" style="color:#FFFF00;">⚠️ Moderate Risk: Some radioactive traces possible.</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="centered-glow" style="color:red;">☢️ High Risk: Potential radioactive contamination detected!</p>', unsafe_allow_html=True)

# ------------------- APP STRUCTURE -------------------
st.markdown('<h1 class="centered-glow">💧☢️ Radioactive Water Contamination Detector</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="centered-glow">Futuristic AI/ML Powered System | Developed by Karthikeyan</h3>', unsafe_allow_html=True)

tabs = st.tabs(["🔬 Contamination Check", "📊 Safety Meter", "⚠️ Radioactive Awareness"])

# ---- TAB 1: Contamination Check ----
with tabs[0]:
    st.subheader("🔍 Enter Water Parameters", anchor=None)
    ph = st.number_input("pH Level", 0.0, 14.0, 7.0)
    tds = st.number_input("TDS (mg/L)", 0.0, 2000.0, 300.0)
    hardness = st.number_input("Hardness (mg/L)", 0.0, 1000.0, 150.0)
    nitrate = st.number_input("Nitrate (mg/L)", 0.0, 500.0, 20.0)
    location = st.text_input("📍 Location")

    if st.button("Run Analysis"):
        score = predict_contamination(ph, tds, hardness, nitrate)
        show_risk_gauge(score)
        show_risk_message(score)

        # Save to dataset
        new_data = pd.DataFrame([[location, ph, tds, hardness, nitrate, score]],
                                columns=["Location", "pH", "TDS", "Hardness", "Nitrate", "RiskScore"])
        try:
            old_data = pd.read_csv("water_data.csv")
            df = pd.concat([old_data, new_data], ignore_index=True)
        except FileNotFoundError:
            df = new_data
        df.to_csv("water_data.csv", index=False)

        st.success("Data saved successfully ✅")
        st.download_button("📥 Download Dataset", data=df.to_csv(index=False),
                           file_name="water_data.csv", mime="text/csv")

# ---- TAB 2: Safety Meter ----
with tabs[1]:
    st.subheader("📊 Safe vs Unsafe Water Levels")
    safe_limits = {"pH": (6.5, 8.5), "TDS": (0, 500), "Hardness": (0, 200), "Nitrate": (0, 45)}
    params = list(safe_limits.keys())
    max_values = [14,2000,1000,500]
    safe_max = [safe_limits[p][1] for p in params]

    fig = go.Figure()
    fig.add_trace(go.Bar(y=params, x=max_values, orientation='h',
                         marker=dict(color='rgba(255,0,0,0.2)'), name="Unsafe Max"))
    fig.add_trace(go.Bar(y=params, x=safe_max, orientation='h',
                         marker=dict(color='rgba(57,255,20,0.7)'), name="Safe Range"))
    fig.update_layout(barmode='overlay', paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#39FF14', family='Bebas Neue'),
                      title="Neon Safe vs Unsafe Levels", xaxis_title="Value", yaxis_title="Parameter")
    st.plotly_chart(fig, use_container_width=True)

# ---- TAB 3: Awareness ----
with tabs[2]:
    st.subheader("⚠️ Dangers of Radioactive Water")
    for i in range(10):
        left = random.randint(0, 90)
        delay = random.uniform(0, 3)
        st.markdown(f"""
        <div style='position: absolute; top: {random.randint(10, 80)}%; left:{left}%;
                    font-size:30px; color:red; animation: floatY 4s ease-in-out {delay}s infinite;'>
            ☢️
        </div>
        """, unsafe_allow_html=True)

    st.write("""
    - ☢️ Radioactive water exposure can cause **cancer, organ damage, and genetic mutations**.  
    - ☠️ Animals and plants also suffer from **biological accumulation** of radioactive isotopes.  
    - 💧 Continuous monitoring is **critical** for human survival.  
    """)

# ----- FOOTER -----
st.markdown("---")
st.markdown('<p class="centered-glow">👨‍💻 Developed by Karthikeyan</p>', unsafe_allow_html=True)
