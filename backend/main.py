from fastapi import FastAPI, Query
import psutil
import requests

app = FastAPI(title="DevNet Global Monitoring System")


# Dictionnaire contenant les villes supportées avec leurs coordonnées GPS et leur pays
CITIES = {
    # 🇹🇳 Tunisie
    "tunis": {"lat": 36.8065, "lon": 10.1815, "country": "Tunisia"},
    "sousse": {"lat": 35.8256, "lon": 10.63699, "country": "Tunisia"},
    "sfax": {"lat": 34.7406, "lon": 10.7603, "country": "Tunisia"},
    "kairouan": {"lat": 35.6781, "lon": 10.0963, "country": "Tunisia"},
    "monastir": {"lat": 35.7643, "lon": 10.8113, "country": "Tunisia"},

    # 🇫🇷 France
    "paris": {"lat": 48.8566, "lon": 2.3522, "country": "France"},
    "lyon": {"lat": 45.7640, "lon": 4.8357, "country": "France"},

    # 🇬🇧 Royaume-Uni
    "london": {"lat": 51.5072, "lon": -0.1276, "country": "UK"},

    # 🇺🇸 États-Unis
    "newyork": {"lat": 40.7128, "lon": -74.0060, "country": "USA"},
    "losangeles": {"lat": 34.0522, "lon": -118.2437, "country": "USA"},

    # 🇦🇪 Émirats Arabes Unis
    "dubai": {"lat": 25.2048, "lon": 55.2708, "country": "UAE"},
}

#  FONCTION MÉTÉO

def fetch_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    return requests.get(url).json()  


# 🖥️ MÉTRIQUES SYSTÈME

@app.get("/api/system")
def system():
    # Retourne l'utilisation actuelle du CPU, de la RAM et du disque dur (en pourcentage)
    return {
        "cpu": psutil.cpu_percent(),           
        "ram": psutil.virtual_memory().percent, 
        "disk": psutil.disk_usage("/").percent  
    }


# MÉTÉO PAR VILLE

@app.get("/api/weather/{city}")
def weather(city: str):
    city = city.lower()  # Convertit le nom de la ville en minuscules pour éviter les erreurs de casse

    if city not in CITIES:
        return {
            "error": "City not found",
            "available": list(CITIES.keys())  #  terje3lk lista 
        }

    # tjik les cooredonne des ville be3d te3ml appe lele fonction meto 
    coords = CITIES[city]
    data = fetch_weather(coords["lat"], coords["lon"])

    # Retourne les informations de la ville avec la météo actuelle
    return {
        "city": city,
        "country": coords["country"],
        "weather": data.get("current_weather", {})  # Retourne un dict vide si la clé n'existe pas
    }


#  LISTE DES VILLES (AVEC FILTRES)

@app.get("/api/cities")
def cities(
    country: str = Query(None),  # filter par pays
    search: str = Query(None)    # cherche ville 
):
    result = CITIES  # On part de la liste complète des villes

    # Si un pays est fourni, on garde seulement les villes de ce pays
    if country:
        result = {k:v for k,v in result.items() if v["country"].lower() == country.lower()}

    # raje3li le recheche 
    if search:
        result = {k:v for k,v in result.items() if search.lower() in k.lower()}

    return result 


#  VÉRIFICATION DE SANTÉ  de api 
@app.get("/api/health")
def health():
    return {"status": "ok"}