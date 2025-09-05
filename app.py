import streamlit as st
import random

st.set_page_config(page_title="Radioactive Water Detector", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
    <style>
    .stApp {
        background-color: #0d0d0d; /* radioactive dark theme */
        position: relative;
        min-height: 100vh; /* allow scroll */
        overflow-x: hidden; /* only stop sideways scroll */
    }

    /* Water drop animation */
    @keyframes fall {
        0% { transform: translateY(-100px); opacity: 1; }
        100% { transform: translateY(110vh); opacity: 0; }
    }
    .drop {
        position: fixed;
        top: -50px;
        color: #00e6e6;
        font-size: 22px;
        animation: fall linear infinite;
        text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
        z-index: 0;
        pointer-events: none;
    }

    /* Radioactive symbol animation */
    @keyframes floatRotate {
        0%   { transform: translateY(0px) rotate(0deg); opacity: 0.7; }
        50%  { transform: translateY(20px) rotate(180deg); opacity: 1; }
        100% { transform: translateY(0px) rotate(360deg); opacity: 0.7; }
    }
    .radio {
        position: fixed;
        font-size: 36px;
        color: #39ff14;
        text-shadow: 0 0 15px #39ff14, 0 0 25px #39ff14;
        animation: floatRotate 6s infinite ease-in-out;
        z-index: 0;
        pointer-events: none;
    }

    /* Centered main title */
    .title {
        text-align: center;
        font-family: 'Bebas Neue', sans-serif;
        color: #39ff14;
        font-size: 48px;
        text-shadow: 0 0 20px #39ff14, 0 0 40px #39ff14;
        margin-top: 20px;
        margin-bottom: 40px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- Animated Background Elements ----------------
# Add 15 falling drops
for i in range(15):
    st.markdown(
        f"<div class='drop' style='left:{random.randint(0,95)}%; animation-duration:{random.uniform(3,7)}s; animation-delay:{random.uniform(0,5)}s;'>💧</div>",
        unsafe_allow_html=True
    )

# Add 6 radioactive floating symbols
for i in range(6):
    st.markdown(
        f"<div class='radio' style='left:{random.randint(5,90)}%; top:{random.randint(10,80)}%; animation-delay:{random.uniform(0,4)}s;'>☢️</div>",
        unsafe_allow_html=True
    )

# ---------------- Main Content ----------------
st.markdown("<div class='title'>💧☢️ Radioactive Water Contamination Detector</div>", unsafe_allow_html=True)

st.write("Futuristic AI/ML Powered System | Developed by **Karthikeyan** ✅")
