import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ===================== APP CONFIG =====================
st.set_page_config(
    page_title="💧 Radioactive Water Detection",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Neon green theme styling
st.markdown("""
    <style>
    body {
        background-color: black;
        color: #39ff14; /* Neon green */
    }
    .stApp {
        background: radial-gradient(circle at top, #001100, #000000);
        color: #39ff14;
    }
    .stTabs [data-baseweb="tab-list"] button {
        color: #39ff14;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ===================== SIDEBAR =====================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/483/483947.png", width=80)
st.sidebar.title("☢️ Water Safety Monitor")
st.sidebar.write("Developed by **Karthikeyan**")

# ===================== TABS =====================
tabs = st.tabs(["🏠 Home", "📊 Input Data", "📈 Comparison", "⚠️ Radioactive Caution"])

# ===================== HOME TAB =====================
with tabs[0]:
    st.title("💧 AI/ML App for Radioactive Water Contamination Detection")
    st.markdown("""
        This application helps in **detecting possible radioactive contamination** 
        in groundwater using water quality parameters.
        
        ⚡ Powered by AI/ML | 🎨 Neon Reactive Theme
    """)
    st.image("https://media.giphy.com/media/3o7abldj0b3rxrZUxW/giphy.gif", caption="Water Safety in Action", use_container_width=True)

# ===================== INPUT TAB =====================
with tabs[1]:
    st.header("📊 Enter Water Quality Parameters")

    pH = st.number_input("pH Level", 0.0, 14.0, 7.0)
    tds = st.number_input("TDS (mg/L)", 0.0, 2000.0, 300.0)
    hardness = st.number_input("Hardness (mg/L)", 0.0, 1000.0, 150.0)
    nitrate = st.number_input("Nitrate (mg/L)", 0.0, 100.0, 20.0)
    location = st.text_input("📍 Location Name", "Chengalpet")

    # Threshold logic
    safe = True
    if not (6.5 <= pH <= 8.5):
        safe = False
    if tds > 500 or hardness > 200 or nitrate > 45:
        safe = False

    if safe:
        st.success("✅ Safe: No significant radioactive contamination detected.")
    else:
        st.error("☢️ Not Safe: Possible radioactive contamination detected!")

    # Save data
    if st.button("💾 Save Data"):
        data = pd.DataFrame([[location, pH, tds, hardness, nitrate, "Safe" if safe else "Not Safe"]],
                            columns=["Location", "pH", "TDS", "Hardness", "Nitrate", "Status"])
        try:
            old_data = pd.read_csv("water_data.csv")
            data = pd.concat([old_data, data], ignore_index=True)
        except:
            pass
        data.to_csv("water_data.csv", index=False)
        st.success("📂 Data saved successfully!")

    # Download data
    try:
        data_file = pd.read_csv("water_data.csv")
        st.download_button("⬇️ Download Data", data_file.to_csv(index=False), "water_data.csv")
    except:
        pass

# ===================== COMPARISON TAB =====================
with tabs[2]:
    st.header("📈 Safe Values vs Your Values")

    safe_values = {"pH": 7.0, "TDS": 500, "Hardness": 200, "Nitrate": 45}
    user_values = {"pH": pH, "TDS": tds, "Hardness": hardness, "Nitrate": nitrate}

    # Safe Graph
    fig_safe = go.Figure(go.Bar(
        x=list(safe_values.keys()),
        y=list(safe_values.values()),
        marker_color="green",
        name="Safe Limits"
    ))
    fig_safe.update_layout(height=250, width=250, title="Safe Values", title_x=0.5)

    # User Graph
    fig_user = go.Figure(go.Bar(
        x=list(user_values.keys()),
        y=list(user_values.values()),
        marker_color="red",
        name="Your Input"
    ))
    fig_user.update_layout(height=250, width=250, title="Your Values", title_x=0.5)

    # Place graphs side by side
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_safe, use_container_width=True)
    with col2:
        st.plotly_chart(fig_user, use_container_width=True)

# ===================== CAUTION TAB =====================
with tabs[3]:
    st.header("⚠️ Caution: Radioactive Contamination in Water")
    st.markdown("""
        Radioactive contamination in water can cause **severe health issues**:

        - ☢️ **Cancer risks** due to long-term exposure  
        - 🧬 **DNA damage and genetic mutations**  
        - 🫁 **Organ damage** (kidney, liver, lungs)  
        - 🐟 **Harmful to aquatic life**  
        - 🐄 **Contaminates livestock & agriculture**  

        Ensuring **clean, safe water** is vital for humans, animals, and the environment.  
    """)
    st.image("radioactive_process.png", width=200)
