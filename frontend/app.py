import streamlit as st
import requests
import time

# =========================
# 🎯 CONFIGURATION PAGE
# =========================
st.set_page_config(
    page_title="DevNet Monitoring Dashboard",
    page_icon="🧠",
    layout="wide"
)

BACKEND_URL = "http://backend:8000"
# =========================
# 🎨 STYLE GLOBAL
# =========================
st.markdown("""
    <style>
        .main {
            background-color: #0e1117;
            color: white;
        }
        h1, h2, h3 {
            color: #00ffcc;
        }
        .metric-box {
            background-color: #1c1f26;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0px 0px 10px rgba(0,255,204,0.2);
        }
    </style>
""", unsafe_allow_html=True)

# =========================
# 🚀 TITRE
# =========================
st.title("🧠 DevNet Intelligent Monitoring System")
st.caption("Real-time System + API Monitoring | DevOps Project")

# =========================
# 🔄 LIVE DASHBOARD
# =========================
placeholder = st.empty()

while True:
    try:
        system = requests.get(f"{BACKEND_URL}/api/system").json()
        weather = requests.get(f"{BACKEND_URL}/api/weather").json()

        with placeholder.container():

            # =========================
            # 📊 SYSTEM METRICS
            # =========================
            st.subheader("📊 System Performance")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("CPU Usage (%)", system["cpu_percent"])

            with col2:
                st.metric("RAM Usage (%)", system["ram"]["percent"])

            with col3:
                st.metric("Disk Usage (%)", system["disk"]["percent"])

            st.divider()

            # =========================
            # 🌤️ WEATHER SECTION
            # =========================
            st.subheader("🌤️ Weather Monitoring (Tunisia)")

            w = weather.get("current_weather", {})

            col4, col5, col6 = st.columns(3)

            with col4:
                st.metric("Temperature (°C)", w.get("temperature", "N/A"))

            with col5:
                st.metric("Wind Speed", w.get("windspeed", "N/A"))

            with col6:
                st.metric("Wind Direction", w.get("winddirection", "N/A"))

            st.divider()

            # =========================
            # 🧠 INFO PANEL
            # =========================
            st.info("🔄 Auto-refresh every 3 seconds | DevNet Dashboard Running")

        time.sleep(3)
        st.rerun()

    except Exception as e:
        st.error("❌ Backend not reachable. Please start FastAPI server.")
        st.code(str(e))
        break