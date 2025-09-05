import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Radioactive Water Contamination Detector", layout="wide")

# ================= CUSTOM CSS =================
css_block = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

* {
  font-family: 'Bebas Neue', sans-serif !important;
}

html, body, [class*="css"] {
  background-color: #0a0a0a;
  color: #e8f5e9;
  min-height: 100vh;
}

/* Title & Subtitle */
h1.app-title {
  text-align: center;
  color: #FFD300; /* Yellow radioactive title */
  font-size: 52px;
  margin-bottom: 4px;
  text-shadow: 0 0 10px #FFD300, 0 0 28px #FF7518;
}
p.app-sub {
  text-align: center;
  color: #39FF14;
  margin-top: 0;
  font-size: 20px;
  text-shadow: 0 0 10px #39FF14;
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

def show_safety_graph(ph, tds, hardness, nitrate):
    safe_ranges = {
        "pH": (6.5, 8.5),
        "TDS": (0, 500),
        "Hardness": (0, 200),
        "Nitrate": (0, 45),
    }
    values = {"pH": ph, "TDS": tds, "Hardness": hardness, "Nitrate": nitrate}

    fig = go.Figure()
    for param, (low, high) in safe_ranges.items():
        fig.add_trace(go.Bar(
            x=[param],
            y=[values[param]],
            name=f"{param} Value",
            marker_color="red" if values[param] < low or values[param] > high else "green"
        ))
        fig.add_trace(go.Bar(
            x=[param],
            y=[high],
            name=f"{param} Safe Max",
            marker_color="lightgreen",
            opacity=0.5
        ))

    fig.update_layout(
        title="Water Quality vs Safe Ranges",
        barmode="overlay",
        yaxis_title="Levels (mg/L or pH)"
    )
    st.plotly_chart(fig, use_container_width=True)

# ================= UI =================
st.markdown("<h1 class='app-title'>💧☢️ Radioactive Water Contamination Detector</h1>", unsafe_allow_html=True)
st.markdown("<p class='app-sub'>AI/ML Powered Water Safety | Developed by Karthikeyan</p>", unsafe_allow_html=True)

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
        if os.path.exists("water_data.csv"):
            old_data = pd.read_csv("water_data.csv")
            df = pd.concat([old_data, new_data], ignore_index=True)
        else:
            df = new_data
        df.to_csv("water_data.csv", index=False)

        st.success("Data saved successfully ✅")
        st.download_button("📥 Download Dataset", data=df.to_csv(index=False),
                           file_name="water_data.csv", mime="text/csv")

# ---- TAB 2 ----
with tabs[1]:
    st.subheader("📊 Safe vs Unsafe Water Levels (Mini Dashboard)")

    safe_ranges = {
        "pH": (6.5, 8.5, ph),
        "TDS (mg/L)": (0, 500, tds),
        "Hardness (mg/L)": (0, 200, hardness),
        "Nitrate (mg/L)": (0, 45, nitrate)
    }

    params = list(safe_ranges.items())

    # Display 2 parameters per row
    for i in range(0, len(params), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j >= len(params):
                break
            param, (low, high, value) = params[i + j]
            
            with col:
                subcols = st.columns([1.1, 1.0, 0.7])  # Graph + value + status

                # Small Bar Graph
                with subcols[0]:
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=[param],
                        y=[value],
                        name=f"{param} Value",
                        marker_color="red" if value < low or value > high else "#39FF14"
                    ))
                    # Safe range overlay
                    fig.add_shape(
                        type="rect",
                        x0=-0.5, x1=0.5,
                        y0=low, y1=high,
                        fillcolor="rgba(57,255,20,0.2)",
                        line_width=0
                    )
                    fig.update_layout(
                        title=f"{param} Level",
                        barmode="overlay",
                        height=180, width=180,
                        margin=dict(l=10, r=10, t=30, b=10)
                    )
                    st.plotly_chart(fig, use_container_width=False)

                # Display Value
                with subcols[1]:
                    st.markdown(
                        f"""
                        <div style="font-size:16px; color:#FFD300;">
                        <b>{param}</b><br>
                        Safe Range: {low} – {high}<br>
                        Your Value: <span style="color:{'red' if value < low or value > high else '#39FF14'};">{value}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # Parameter Status
                with subcols[2]:
                    status = "✅ Safe" if low <= value <= high else "⚠️ Unsafe"
                    color = "#39FF14" if low <= value <= high else "red"
                    st.markdown(
                        f"<div style='font-size:18px; color:{color};'><b>{status}</b></div>",
                        unsafe_allow_html=True
                    )

    st.info("ℹ️ Compare your water parameters above with the WHO safe ranges.")


# ---- TAB 3 ----
with tabs[2]:
    st.subheader("⚠️ Dangers of Radioactive Water")
    st.image("radioactive_process.png", caption="Radioactive Contamination Process")
    st.write("""
    - ☢️ Radioactive water exposure can cause **cancer, organ damage, and genetic mutations**.  
    - ☠️ Animals and plants also suffer from **biological accumulation** of radioactive isotopes.  
    - 💧 Continuous monitoring is **critical** for human survival.  
    """)

st.markdown("---")
st.markdown('<p style="text-align:center; color:#FFD300;">👨‍💻 Developed by Karthikeyan</p>', unsafe_allow_html=True)

