import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# =========================
# 1. Configuration de la page
# =========================
st.set_page_config(
    page_title="DevNet Global Dashboard",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BACKEND = "http://localhost:8000"

# =========================
# 2. 🎨 CSS GLOBAL (Design Premium "Glassmorphism")
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;500;700;800&display=swap');
    
    /* Fond global : Dégradé bleu nuit très profond, pas noir pur */
    .stApp {
        background: radial-gradient(circle at top, #1a202c 0%, #0f172a 100%);
        color: #e2e8f0;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Style des titres de section avec effet lumineux */
    .section-label {
        color: #94a3b8;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-top: 30px;
        margin-bottom: 20px;
        padding-bottom: 5px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Style du Header */
    .header-main { 
        font-size: 26px; 
        font-weight: 800; 
        background: -webkit-linear-gradient(45deg, #00f2ff, #0066ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 20px rgba(0, 242, 255, 0.2);
    }
    
    .status-online { 
        color: #10b981; font-size: 11px; font-weight: 800; 
        background: rgba(16, 185, 129, 0.1); 
        padding: 5px 12px; border-radius: 20px; 
        border: 1px solid rgba(16, 185, 129, 0.3);
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.2);
    }
    
    .status-offline { 
        color: #ef4444; font-size: 11px; font-weight: 800; 
        background: rgba(239, 68, 68, 0.1); 
        padding: 5px 12px; border-radius: 20px; 
        border: 1px solid rgba(239, 68, 68, 0.3);
        box-shadow: 0 0 10px rgba(239, 68, 68, 0.2);
    }

    /* Cartes Météo (Style Verre / 3D Premium) */
    .weather-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.9));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
    }
    .weather-card:hover { 
        transform: translateY(-5px) scale(1.02); 
        border-color: rgba(0, 242, 255, 0.4); 
        box-shadow: 0 15px 35px -5px rgba(0, 242, 255, 0.15);
    }
    
    .card-city { color: #f8fafc; font-size: 16px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;}
    .card-country { color: #64748b; font-size: 11px; font-weight: 500;}
    .card-temp { font-size: 36px; font-weight: 800; margin: 10px 0; text-shadow: 0 2px 10px rgba(0,0,0,0.3);}
    .card-detail { color: #94a3b8; font-size: 11px; margin: 2px 0; font-weight: 500;}

    /* Conteneurs (Tableau etc) */
    .glass-container {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 15px;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.2);
    }

    /* Boutons stylisés */
    .stButton>button {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        color: #e2e8f0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
        width: 100%;
        padding: 10px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #00f2ff, #0066ff);
        color: #fff;
        border-color: transparent;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# =========================
# 3. 📟 HEADER SECTION (Dynamique)
# =========================
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown('<div class="header-main">⚡ DEVNET GLOBAL COMMAND CENTER</div>', unsafe_allow_html=True)

backend_online = False
try:
    requests.get(f"{BACKEND}/api/health", timeout=2)
    backend_online = True
    with col2:
        st.markdown('<div style="text-align:right"><span class="status-online">● SYSTEM ONLINE</span></div>', unsafe_allow_html=True)
except:
    with col2:
        st.markdown('<div style="text-align:right"><span class="status-offline">● SYSTEM OFFLINE</span></div>', unsafe_allow_html=True)

st.write("")

# =========================
# 4. 🖥️ SYSTEM METRICS (Dynamique)
# =========================
st.markdown('<div class="section-label">System Performance</div>', unsafe_allow_html=True)

if backend_online:
    try:
        sys = requests.get(f"{BACKEND}/api/system").json()
        g1, g2, g3, g4 = st.columns(4)
        
        metrics_config = [
            {"val": sys.get('cpu', 0), "label": "CPU LOAD", "color": "#00f2ff"}, # Cyan Neon
            {"val": sys.get('ram', 0), "label": "RAM USAGE", "color": "#f43f5e"}, # Rose/Rouge néon
            {"val": sys.get('disk', 0), "label": "DISK SPACE", "color": "#fbbf24"}, # Jaune/Or
            {"val": sys.get('net', 0), "label": "NET TRAFFIC", "color": "#a855f7"} # Violet néon
        ]
        
        def create_dial_gauge(value, label, color):
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = value,
                domain = {'x': [0, 1], 'y': [0, 1]},
                number = {'font': {'color': '#f8fafc', 'size': 28, 'family': 'JetBrains Mono', 'weight': 'bold'}, 'suffix': "%"},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#334155", 'tickvals': [0, 50, 100]},
                    'bar': {'color': color, 'thickness': 0.85},
                    'bgcolor': "rgba(0,0,0,0)", 
                    'borderwidth': 0,
                    'steps': [
                        {'range': [0, 100], 'color': 'rgba(255,255,255,0.03)'},
                        {'range': [85, 100], 'color': 'rgba(244, 63, 94, 0.15)'} 
                    ],
                }
            ))
            fig.update_layout(
                title = {'text': label, 'font': {'size': 12, 'color': '#94a3b8', 'family': 'JetBrains Mono', 'weight': 'bold'}},
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                height=180, margin=dict(l=15, r=15, t=50, b=10)
            )
            return fig

        with g1: st.plotly_chart(create_dial_gauge(metrics_config[0]['val'], metrics_config[0]['label'], metrics_config[0]['color']), use_container_width=True, config={'displayModeBar': False})
        with g2: st.plotly_chart(create_dial_gauge(metrics_config[1]['val'], metrics_config[1]['label'], metrics_config[1]['color']), use_container_width=True, config={'displayModeBar': False})
        with g3: st.plotly_chart(create_dial_gauge(metrics_config[2]['val'], metrics_config[2]['label'], metrics_config[2]['color']), use_container_width=True, config={'displayModeBar': False})
        with g4: st.plotly_chart(create_dial_gauge(metrics_config[3]['val'], metrics_config[3]['label'], metrics_config[3]['color']), use_container_width=True, config={'displayModeBar': False})
    except Exception as e:
        st.error(f"Erreur de lecture des métriques : {e}")
else:
    st.error("⚠️ Backend Offline. Lancez le serveur FastAPI.")

st.write("")

# =========================
# 5. 🌍 CITY REGISTRY & DISTRIBUTION
# =========================
st.markdown('<div class="section-label">Node Registry & Network</div>', unsafe_allow_html=True)
col_left, col_right = st.columns([2.5, 1])

f_df = pd.DataFrame()
dynamic_temperatures = {} 

if backend_online:
    with col_left:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        data = requests.get(f"{BACKEND}/api/cities").json()
        df_main = pd.DataFrame([{"City": k.capitalize(), "Country": v["country"], "Coords": f"{v.get('lat', '0')}, {v.get('lon', '0')}"} for k, v in data.items()])
        
        f1, f2 = st.columns([1.5, 1])
        search = f1.text_input("Search...", label_visibility="collapsed", placeholder="🔍 Search city...")
        country_opts = ["All countries"] + sorted(df_main["Country"].unique().tolist())
        c_filter = f2.selectbox("All Countries", country_opts, label_visibility="collapsed")
        
        f_df = df_main.copy()
        if search: f_df = f_df[f_df["City"].str.contains(search, case=False)]
        if c_filter != "All countries": f_df = f_df[f_df["Country"] == c_filter]
        
        st.dataframe(f_df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="glass-container" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown('<div style="color:#94a3b8; font-size:12px; font-weight:bold; margin-bottom:10px;">NODE DISTRIBUTION</div>', unsafe_allow_html=True)
        counts = f_df["Country"].value_counts()
        for country, val in counts.items():
            st.markdown(f'<div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:2px;"><span>{country}</span><span style="color:#00f2ff; font-weight:bold;">{val}</span></div>', unsafe_allow_html=True)
            st.progress(min(val/10, 1.0))
        st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# =========================
# 6. 🌤️ LIVE WEATHER DASHBOARD (Grid Premium)
# =========================
st.markdown('<div class="section-label">Live Environment Telemetry</div>', unsafe_allow_html=True)

if not f_df.empty:
    w_cols = st.columns(4)
    priority_cities = ["Tunis", "Sousse", "Sfax", "Kairouan", "Monastir", "Paris", "Lyon", "London", "New York", "Los Angeles", "Dubai"]
    weather_df = f_df.copy()
    weather_df['Priority'] = weather_df['City'].apply(lambda x: priority_cities.index(x) if x in priority_cities else 99)
    weather_df = weather_df.sort_values('Priority')

    for i, (_, row) in enumerate(weather_df.iterrows()):
        city_slug = row['City'].lower().replace(" ", "")
        try:
            w_res = requests.get(f"{BACKEND}/api/weather/{city_slug}").json()
            w_data = w_res.get("weather", {})
            temp = w_data.get('temperature', '--')
            
            if temp != '--': dynamic_temperatures[row['City']] = float(temp)
            
            # Dégradé de couleur pour la température (froid = cyan, chaud = or/orange)
            t_color = "#fbbf24" if temp != '--' and float(temp) > 25 else "#00f2ff"
            
            with w_cols[i % 4]:
                st.markdown(f"""
                <div class="weather-card">
                    <div class="card-city">{row['City']}</div>
                    <div class="card-country">{row['Country']}</div>
                    <div class="card-temp" style="color:{t_color}">{temp}°C</div>
                    <p class="card-detail">💨 Wind: <span style="color:#e2e8f0">{w_data.get('windspeed', '--')} km/h</span></p>
                    <p class="card-detail">🧭 Direction: <span style="color:#e2e8f0">{w_data.get('winddirection', '--')}°</span></p>
                </div>
                """, unsafe_allow_html=True)
        except: continue

st.write("")

# =========================
# 7. 📊 ANALYTICS & REPORTS 
# =========================
st.markdown('<div class="section-label">Global Analytics</div>', unsafe_allow_html=True)
a1, a2 = st.columns(2)

if not f_df.empty:
    with a1:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        stats_c = f_df["Country"].value_counts().reset_index()
        stats_c.columns = ["Country", "Count"]

        fig_bars = px.bar(stats_c, x="Country", y="Count", color="Country", 
                          color_discrete_sequence=["#00f2ff", "#f43f5e", "#fbbf24", "#a855f7", "#10b981"])
        
        fig_bars.update_layout(
            title = {'text': "Nodes Deployed per Region", 'font': {'size': 14, 'color': '#f8fafc'}},
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color="#94a3b8", font_family='JetBrains Mono', height=300,
            margin=dict(l=0, r=0, t=40, b=0), showlegend=False,
            xaxis=dict(showgrid=False, title=""), yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title="")
        )
        st.plotly_chart(fig_bars, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    with a2:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        if dynamic_temperatures:
            trend_data = pd.DataFrame(list(dynamic_temperatures.items()), columns=['City', 'Temp'])
            fig_trend = px.area(trend_data, x='City', y='Temp', markers=True)
            
            fig_trend.update_traces(
                line=dict(color='#00f2ff', width=3), 
                marker=dict(size=8, color='#fff', symbol='circle'),
                fillcolor='rgba(0, 242, 255, 0.1)'
            )
            fig_trend.update_layout(
                title = {'text': "Live Temperature Stream (°C)", 'font': {'size': 14, 'color': '#f8fafc'}},
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                font_color="#94a3b8", font_family='JetBrains Mono', height=300, 
                margin=dict(l=0,r=0,t=40,b=0), xaxis=dict(showgrid=False, title=""), 
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="")
            )
            st.plotly_chart(fig_trend, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No temperature data available.")
        st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 8. 🔗 QUICK ACCESS & FOOTER
# =========================
st.markdown('<div class="section-label">System Controls</div>', unsafe_allow_html=True)
b1, b2, b3 = st.columns([1.5, 1, 1])
b1.code(f"API Target: {BACKEND}", language="bash")
if b2.button("🔄 Sync Live Data"):
    st.rerun()
b3.button("⚙️ System Settings")

st.write("---")
st.markdown('<div style="text-align:center; color:#64748b; font-size:11px; margin-top:20px;">🚀 DevNet Global Command Center v3.0 | FastAPI + Streamlit | Premium Edition</div>', unsafe_allow_html=True)