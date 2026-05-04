import streamlit as st
import requests
import pandas as pd

BACKEND = "http://localhost:8000"

st.set_page_config(
    page_title="DevNet Global Dashboard",
    page_icon="🧠",
    layout="wide"
)

# =========================
# 🎨 STYLE
# =========================
st.markdown("""
<style>
.card {
    background: linear-gradient(145deg, #1c1f26, #14161b);
    padding: 18px;
    border-radius: 16px;
    margin: 10px;
    box-shadow: 0 0 12px rgba(0,255,204,0.15);
    text-align: center;
}
.title { color: #00ffcc; font-size: 20px; }
.small { color: #aaa; }
</style>
""", unsafe_allow_html=True)

st.title("🧠 DevNet Global Monitoring Dashboard")

# =========================
# 🖥️ SYSTEM METRICS
# =========================
try:
    sys = requests.get(f"{BACKEND}/api/system").json()

    c1, c2, c3 = st.columns(3)

    c1.metric("CPU", f"{sys['cpu']}%")
    c2.metric("RAM", f"{sys['ram']}%")
    c3.metric("DISK", f"{sys['disk']}%")

except:
    st.error("❌ Backend not running")

st.divider()

# =========================
# 🌍 GET ALL CITIES
# =========================
data = requests.get(f"{BACKEND}/api/cities").json()

cities_list = [
    {"name": k, "country": v["country"]}
    for k, v in data.items()
]

df = pd.DataFrame(cities_list)

# =========================
# 🔎 FILTERS
# =========================
col1, col2 = st.columns(2)

with col1:
    search = st.text_input("🔎 Search city")

with col2:
    countries = sorted(df["country"].unique())
    country_filter = st.selectbox("🌍 Filter by country", ["All"] + countries)

# apply filters
if search:
    df = df[df["name"].str.contains(search.lower(), case=False)]

if country_filter != "All":
    df = df[df["country"] == country_filter]

# =========================
# 📊 CHARTS (IMPORTANT)
# =========================
st.subheader("📊 Countries Statistics")

country_stats = df["country"].value_counts()

st.bar_chart(country_stats)

# =========================
# 🌍 WEATHER CARDS GRID
# =========================
st.subheader("🌤️ Live Weather Dashboard")

cols = st.columns(3)

for i, row in df.iterrows():

    try:
        res = requests.get(f"{BACKEND}/api/weather/{row['name']}").json()
        w = res.get("weather", {})

        cols[i % 3].markdown(f"""
        <div class="card">
            <div class="title">🌍 {row['name'].upper()}</div>
            <div class="small">{row['country']}</div>
            <h3>🌡️ {w.get('temperature', 'N/A')} °C</h3>
            <p>💨 {w.get('windspeed', 'N/A')} km/h</p>
            <p>🧭 {w.get('winddirection', 'N/A')}°</p>
        </div>
        """, unsafe_allow_html=True)

    except:
        cols[i % 3].error(f"Error {row['name']}")

# =========================
# 📊 PIE CHART (BONUS PRO)
# =========================
st.subheader("🥧 Countries Distribution")

st.pyplot(df["country"].value_counts().plot.pie(autopct="%1.1f%%").figure)

# =========================
# FOOTER
# =========================
st.caption("🚀 DevNet Dashboard | FastAPI + Streamlit + Docker | Engineer Level")