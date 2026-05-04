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
# 🎨 STYLE MODERNE
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

        .card {
            background: linear-gradient(145deg, #1c1f26, #14171c);
            padding: 18px;
            border-radius: 15px;
            box-shadow: 0px 0px 12px rgba(0,255,204,0.15);
        }

        .stMetric {
            background-color: #1c1f26;
            border-radius: 12px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# =========================
# 🚀 TITLE
# =========================
st.title("🧠 DevNet Intelligent Monitoring System")
st.caption("Real-time System + Multi-City Weather | DevOps Project")

placeholder = st.empty()

# =========================
# 🔄 LIVE LOOP
# =========================
while True:
    try:
        system = requests.get(f"{BACKEND_URL}/api/system").json()

        weather_sousse = requests.get(f"{BACKEND_URL}/api/weather/sousse").json()
        weather_kairouan = requests.get(f"{BACKEND_URL}/api/weather/kairouan").json()

        with placeholder.container():

            # =========================
            # 📊 SYSTEM
            # =========================
            st.subheader("📊 System Monitoring")

            col1, col2, col3 = st.columns(3)

            col1.metric("CPU (%)", system["cpu_percent"])
            col2.metric("RAM (%)", system["ram"]["percent"])
            col3.metric("Disk (%)", system["disk"]["percent"])

            st.divider()

            # =========================
            # 🌤️ WEATHER
            # =========================
            st.subheader("🌤️ Weather Monitoring - Tunisia")

            col4, col5 = st.columns(2)

            # 🌤️ SOUSSE
            with col4:
                st.markdown("### 🌊 Sousse")
                w = weather_sousse.get("current_weather", {})
                st.metric("Temp (°C)", w.get("temperature", "N/A"))
                st.metric("Wind Speed", w.get("windspeed", "N/A"))

            # 🌤️ KAIROUAN
            with col5:
                st.markdown("### 🕌 Kairouan")
                w2 = weather_kairouan.get("current_weather", {})
                st.metric("Temp (°C)", w2.get("temperature", "N/A"))
                st.metric("Wind Speed", w2.get("windspeed", "N/A"))

            st.divider()

            st.info("🔄 Auto-refresh every 3 seconds | DevNet Dashboard Running")

        time.sleep(3)
        st.rerun()

    except Exception as e:
        st.error("❌ Backend not reachable")
        st.code(str(e))
        break