import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


st.set_page_config(
    page_title="DevNet Global Dashboard",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BACKEND = "http://localhost:8000"


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;500;700;800&display=swap');
    
    /* Fond sombre avec dégradé radial pour toute la page */
    .stApp {
        background: radial-gradient(circle at top, #1a202c 0%, #0f172a 100%);
        color: #e2e8f0;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Style des titres de section (petits textes en majuscules) */
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

    /* Titre principal avec effet dégradé bleu cyan */
    .header-main { 
        font-size: 26px; 
        font-weight: 800; 
        background: -webkit-linear-gradient(45deg, #00f2ff, #0066ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 20px rgba(0, 242, 255, 0.2);
    }
    
    /* Badge vert quand le système est en ligne */
    .status-online { 
        color: #10b981; font-size: 11px; font-weight: 800; 
        background: rgba(16, 185, 129, 0.1); 
        padding: 5px 12px; border-radius: 20px; 
        border: 1px solid rgba(16, 185, 129, 0.3);
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.2);
    }
    
    /* Badge rouge quand le système est hors ligne */
    .status-offline { 
        color: #ef4444; font-size: 11px; font-weight: 800; 
        background: rgba(239, 68, 68, 0.1); 
        padding: 5px 12px; border-radius: 20px; 
        border: 1px solid rgba(239, 68, 68, 0.3);
        box-shadow: 0 0 10px rgba(239, 68, 68, 0.2);
    }

    /* Carte météo avec effet verre (glassmorphism) */
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
    /* Effet au survol : légère élévation et bordure cyan */
    .weather-card:hover { 
        transform: translateY(-5px) scale(1.02); 
        border-color: rgba(0, 242, 255, 0.4); 
        box-shadow: 0 15px 35px -5px rgba(0, 242, 255, 0.15);
    }
    
    /* Styles des textes à l'intérieur des cartes météo */
    .card-city { color: #f8fafc; font-size: 16px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;}
    .card-country { color: #64748b; font-size: 11px; font-weight: 500;}
    .card-temp { font-size: 36px; font-weight: 800; margin: 10px 0; text-shadow: 0 2px 10px rgba(0,0,0,0.3);}
    .card-detail { color: #94a3b8; font-size: 11px; margin: 2px 0; font-weight: 500;}

    /* Conteneur avec fond semi-transparent pour les tableaux et graphiques */
    .glass-container {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 15px;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.2);
    }

    /* Style des boutons */
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
    /* Bouton en survol : dégradé bleu cyan */
    .stButton>button:hover {
        background: linear-gradient(135deg, #00f2ff, #0066ff);
        color: #fff;
        border-color: transparent;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.4);
    }
</style>
""", unsafe_allow_html=True)


#  RÉCUPÉRATION ET MISE EN CACHE DES DONNÉES

@st.cache_data(ttl=60)  # Les métriques système sont mises en cache 60 secondes pour ne pas surcharger l'API
def fetch_system_metrics():
    try:
        return requests.get(f"{BACKEND}/api/system", timeout=2).json()
    except requests.exceptions.RequestException:
        return None  

@st.cache_data(ttl=300)  # La liste des villes est mise en cache 5 minutes 
def fetch_cities_data():
    try:
        data = requests.get(f"{BACKEND}/api/cities", timeout=3).json()
        # card des villes 
        return pd.DataFrame([{
            "City": k.capitalize(), 
            "Country": v["country"], 
            "lat": float(v.get('lat', 0)),  # Latitude pour la carte 
            "lon": float(v.get('lon', 0))   # Longitude pour la carte
        } for k, v in data.items()])
    except requests.exceptions.RequestException:
        return pd.DataFrame()  

#  EN-TÊTE DE LA PAGE

# tableau 
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown('<div class="header-main">⚡ DEVNET GLOBAL COMMAND CENTER</div>', unsafe_allow_html=True)

# kan el bakend fonctionne et tout va bien  en appelant l'endpoint /api/health
backend_online = False
try:
    requests.get(f"{BACKEND}/api/health", timeout=2)
    backend_online = True
    with col2:
        st.markdown('<div style="text-align:right"><span class="status-online">● SYSTEM ONLINE</span></div>', unsafe_allow_html=True)
except requests.exceptions.RequestException:
    # Si le serveur ne répond pas, on affiche le badge rouge
    with col2:
        st.markdown('<div style="text-align:right"><span class="status-offline">● SYSTEM OFFLINE</span></div>', unsafe_allow_html=True)

#  MÉTRIQUES SYSTÈME

st.markdown('<div class="section-label">my system performance</div>', unsafe_allow_html=True)

if backend_online:
    sys = fetch_system_metrics()
    if sys:
        
        g1, g2, g3, g4 = st.columns(4)
        metrics_config = [
            {"val": sys.get('cpu', 0),  "label": "CPU LOAD",    "color": "#00f2ff"},
            {"val": sys.get('ram', 0),  "label": "RAM USAGE",   "color": "#f43f5e"},
            {"val": sys.get('disk', 0), "label": "DISK SPACE",  "color": "#fbbf24"},
            {"val": sys.get('net', 0),  "label": "NET TRAFFIC", "color": "#a855f7"}
        ]
        
        def create_dial_gauge(value, label, color):
            # Crée une jauge circulaire Plotly avec une valeur en pourcentage
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = value, domain = {'x': [0, 1], 'y': [0, 1]},
                number = {'font': {'color': '#f8fafc', 'size': 28, 'family': 'JetBrains Mono', 'weight': 'bold'}, 'suffix': "%"},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#334155", 'tickvals': [0, 50, 100]},
                    'bar': {'color': color, 'thickness': 0.85},
                    'bgcolor': "rgba(0,0,0,0)", 'borderwidth': 0,
                    # en rouge  de 85% alert 
                    'steps': [
                        {'range': [0, 100],  'color': 'rgba(255,255,255,0.03)'},
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

        # Affichage des 4 jauges dans leurs colonnes respectives
        with g1: st.plotly_chart(create_dial_gauge(metrics_config[0]['val'], metrics_config[0]['label'], metrics_config[0]['color']), use_container_width=True, config={'displayModeBar': False})
        with g2: st.plotly_chart(create_dial_gauge(metrics_config[1]['val'], metrics_config[1]['label'], metrics_config[1]['color']), use_container_width=True, config={'displayModeBar': False})
        with g3: st.plotly_chart(create_dial_gauge(metrics_config[2]['val'], metrics_config[2]['label'], metrics_config[2]['color']), use_container_width=True, config={'displayModeBar': False})
        with g4: st.plotly_chart(create_dial_gauge(metrics_config[3]['val'], metrics_config[3]['label'], metrics_config[3]['color']), use_container_width=True, config={'displayModeBar': False})
    else:
        st.error("Erreur : Impossible de lire les métriques système.")
else:
    st.error("⚠️ Backend Offline. Lancez le serveur FastAPI.")

#  CARTE MONDIALE ET REGISTRE DES VILLES

st.markdown('<div class="section-label">Global Node Geography</div>', unsafe_allow_html=True)

f_df = pd.DataFrame()         # Tableau filtré 
dynamic_temperatures = {}     # Dictionnaire pour stocker les températures récupérées dynamiquement

if backend_online:
    df_main = fetch_cities_data()
    
    if not df_main.empty:
        # Carte interactive avec les points GPS de chaque ville
        map_fig = px.scatter_mapbox(
            df_main, lat="lat", lon="lon", hover_name="City", hover_data=["Country"],
            color_discrete_sequence=["#00f2ff"], zoom=1.5, height=400
        )
        map_fig.update_layout(
            mapbox_style="carto-darkmatter",  
            margin={"r":0,"t":0,"l":0,"b":0},
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(map_fig, use_container_width=True)

        st.markdown('<div class="section-label">Node Registry & Distribution</div>', unsafe_allow_html=True)
        col_left, col_right = st.columns([2.5, 1])

        with col_left:
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            f1, f2 = st.columns([1.5, 1])
            # Champ de recherche par nom de ville
            search = f1.text_input("Search...", label_visibility="collapsed", placeholder="🔍 Search city...")
            # Menu déroulant pour filtrer par pays
            country_opts = ["All countries"] + sorted(df_main["Country"].unique().tolist())
            c_filter = f2.selectbox("All Countries", country_opts, label_visibility="collapsed")
            
            # Application des filtres sur le tableau principal
            f_df = df_main.copy()
            if search:
                f_df = f_df[f_df["City"].str.contains(search, case=False)]  # Filtre insensible à la casse
            if c_filter != "All countries":
                f_df = f_df[f_df["Country"] == c_filter]
            
            # On affiche seulement le nom et le pays 
            st.dataframe(f_df[["City", "Country"]], use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_right:
            st.markdown('<div class="glass-container" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown('<div style="color:#94a3b8; font-size:12px; font-weight:bold; margin-bottom:10px;">NODE DISTRIBUTION</div>', unsafe_allow_html=True)
            # Compte le nombre de villes par pays et affiche une barre de progression pour chacun
            counts = f_df["Country"].value_counts()
            for country, val in counts.items():
                st.markdown(f'<div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:2px;"><span>{country}</span><span style="color:#00f2ff; font-weight:bold;">{val}</span></div>', unsafe_allow_html=True)
                st.progress(min(val/10, 1.0))  
            st.markdown('</div>', unsafe_allow_html=True)

# TABLEAU DE BORD MÉTÉO EN DIRECT 
st.markdown('<div class="section-label">Live Environment Telemetry</div>', unsafe_allow_html=True)

if not f_df.empty:
    w_cols = st.columns(4)  # 4 cartes par ligne
    priority_cities = ["Tunis", "Sousse", "Sfax", "Kairouan", "Monastir", "Paris", "Lyon", "London", "New York", "Los Angeles", "Dubai"]
    weather_df = f_df.copy()
    # On attribue un rang à chaque ville selon la liste prioritaire (99 = non prioritaire)
    weather_df['Priority'] = weather_df['City'].apply(lambda x: priority_cities.index(x) if x in priority_cities else 99)
    weather_df = weather_df.sort_values('Priority')

    for i, (_, row) in enumerate(weather_df.iterrows()):
        # On convertit le nom de la ville en format compatible avec l'API (minuscules, sans espaces)
        city_slug = row['City'].lower().replace(" ", "")
        try:
            w_res = requests.get(f"{BACKEND}/api/weather/{city_slug}", timeout=2).json()
            w_data = w_res.get("weather", {})
            temp = w_data.get('temperature', '--')
            
            # On stocke la température pour le graphique de tendance 
            if temp != '--':
                dynamic_temperatures[row['City']] = float(temp)
            
            # Couleur de la température : orange si > 25°C, bleu sinon
            t_color = "#fbbf24" if temp != '--' and float(temp) > 25 else "#00f2ff"
            
            # Affichage de la carte météo dans la bonne colonne (rotation circulaire sur 4)
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
        except requests.exceptions.RequestException: 
            continue  # On ignore les villes dont la météo est inaccessible

# ANALYTIQUES ET RAPPORTS
st.markdown('<div class="section-label">Global Analytics</div>', unsafe_allow_html=True)
a1, a2 = st.columns(2)

if not f_df.empty:
    with a1:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        # Compte le nombre de villes par pays pour le graphique en barres
        stats_c = f_df["Country"].value_counts().reset_index()
        stats_c.columns = ["Country", "Count"]

        fig_bars = px.bar(stats_c, x="Country", y="Count", color="Country", 
                          color_discrete_sequence=["#00f2ff", "#f43f5e", "#fbbf24", "#a855f7", "#10b981"])
        
        fig_bars.update_layout(
            title = {'text': "Nodes Deployed per Region", 'font': {'size': 14, 'color': '#f8fafc'}},
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color="#94a3b8", font_family='JetBrains Mono', height=300,
            margin=dict(l=0, r=0, t=40, b=0), showlegend=False,
            xaxis=dict(showgrid=False, title=""),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title="")
        )
        st.plotly_chart(fig_bars, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    with a2:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        if dynamic_temperatures:
            # Graphique de courbe avec les températures de toutes les villes affichées
            trend_data = pd.DataFrame(list(dynamic_temperatures.items()), columns=['City', 'Temp'])
            fig_trend = px.area(trend_data, x='City', y='Temp', markers=True)
            
            fig_trend.update_traces(
                line=dict(color='#00f2ff', width=3), 
                marker=dict(size=8, color='#fff', symbol='circle'),
                fillcolor='rgba(0, 242, 255, 0.1)'  # Zone remplie semi-transparente sous la courbe
            )
            fig_trend.update_layout(
                title = {'text': "Live Temperature Stream (°C)", 'font': {'size': 14, 'color': '#f8fafc'}},
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                font_color="#94a3b8", font_family='JetBrains Mono', height=300, 
                margin=dict(l=0,r=0,t=40,b=0),
                xaxis=dict(showgrid=False, title=""), 
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="")
            )
            st.plotly_chart(fig_trend, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No temperature data available.")
        st.markdown('</div>', unsafe_allow_html=True)

#  CONTRÔLES ET PIED DE PAGE

st.markdown('<div class="section-label">System Controls</div>', unsafe_allow_html=True)
b1, b2, b3 = st.columns([1.5, 1, 1])
b1.code(f"API Target: {BACKEND}", language="bash")  # Affiche l'URL du backend en style code

# Bouton pour forcer le rechargement complet de la page et des données
if b2.button("🔄 Sync Live Data"):
    st.rerun()

b3.button("⚙️ System Settings")  

st.write("---")
st.markdown('<div style="text-align:center; color:#64748b; font-size:11px; margin-top:20px;">🚀 DevNet Global Command Center v3.1 | FastAPI + Streamlit | Premium Edition</div>', unsafe_allow_html=True)