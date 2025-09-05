import streamlit as st

# Inject custom CSS + animations
st.markdown("""
    <style>
    /* Background color */
    body {
        background-color: #0d0d0d; /* deep black radioactive theme */
        overflow: hidden;
    }

    /* Falling water drops animation */
    @keyframes fall {
        0% { transform: translateY(-100px); opacity: 1; }
        100% { transform: translateY(110vh); opacity: 0; }
    }

    .drop {
        position: fixed;
        top: -50px;
        color: #00e6e6; /* cyan glow */
        font-size: 24px;
        animation: fall linear infinite;
        text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
        z-index: -1; /* behind everything */
    }

    /* Radioactive floating + rotation */
    @keyframes floatRotate {
        0%   { transform: translateY(0px) rotate(0deg);   opacity: 0.8; }
        50%  { transform: translateY(20px) rotate(180deg); opacity: 1; }
        100% { transform: translateY(0px) rotate(360deg);  opacity: 0.8; }
    }

    .radio {
        position: fixed;
        font-size: 40px;
        color: #39ff14; /* neon green */
        animation: floatRotate 8s ease-in-out infinite;
        text-shadow: 0 0 10px #39ff14, 0 0 20px #39ff14, 0 0 40px #39ff14;
        z-index: -1; /* behind everything */
    }
    </style>

    <!-- Water Drops -->
    <div class="drop" style="left:5%; animation-duration: 6s;">💧</div>
    <div class="drop" style="left:20%; animation-duration: 8s;">💧</div>
    <div class="drop" style="left:50%; animation-duration: 10s;">💧</div>
    <div class="drop" style="left:70%; animation-duration: 7s;">💧</div>
    <div class="drop" style="left:90%; animation-duration: 9s;">💧</div>
    <div class="drop" style="left:35%; animation-duration: 11s;">💧</div>

    <!-- Radioactive Hazard Symbols -->
    <div class="radio" style="top:20%; left:10%;">☢️</div>
    <div class="radio" style="top:60%; left:80%;">☢️</div>
    <div class="radio" style="top:40%; left:50%;">☢️</div>
    <div class="radio" style="top:75%; left:25%;">☢️</div>
""", unsafe_allow_html=True)

# Example header
st.markdown("<h1 style='text-align: center; color: white; font-family: Bebas Neue;'>💧☢️ Radioactive Water Contamination Detector</h1>", unsafe_allow_html=True)
