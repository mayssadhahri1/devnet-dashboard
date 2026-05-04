from fastapi import FastAPI, Query
import psutil
import requests

app = FastAPI(title="DevNet Global Monitoring System")

# =========================
# 🌍 FULL WORLD CITIES
# =========================
CITIES = {
    # 🇹🇳 Tunisia
    "tunis": {"lat": 36.8065, "lon": 10.1815, "country": "Tunisia"},
    "sousse": {"lat": 35.8256, "lon": 10.63699, "country": "Tunisia"},
    "sfax": {"lat": 34.7406, "lon": 10.7603, "country": "Tunisia"},
    "kairouan": {"lat": 35.6781, "lon": 10.0963, "country": "Tunisia"},
    "monastir": {"lat": 35.7643, "lon": 10.8113, "country": "Tunisia"},

    # 🇫🇷 France
    "paris": {"lat": 48.8566, "lon": 2.3522, "country": "France"},
    "lyon": {"lat": 45.7640, "lon": 4.8357, "country": "France"},

    # 🇬🇧 UK
    "london": {"lat": 51.5072, "lon": -0.1276, "country": "UK"},

    # 🇺🇸 USA
    "newyork": {"lat": 40.7128, "lon": -74.0060, "country": "USA"},
    "losangeles": {"lat": 34.0522, "lon": -118.2437, "country": "USA"},

    # 🇦🇪 UAE
    "dubai": {"lat": 25.2048, "lon": 55.2708, "country": "UAE"},
}

# =========================
# 🌤️ WEATHER FUNCTION
# =========================
def fetch_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    return requests.get(url).json()

# =========================
# 🖥️ SYSTEM METRICS
# =========================
@app.get("/api/system")
def system():
    return {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent
    }

# =========================
# 🌤️ WEATHER BY CITY (FIXED)
# =========================
@app.get("/api/weather/{city}")
def weather(city: str):
    city = city.lower()

    if city not in CITIES:
        return {
            "error": "City not found",
            "available": list(CITIES.keys())
        }

    coords = CITIES[city]
    data = fetch_weather(coords["lat"], coords["lon"])

    return {
        "city": city,
        "country": coords["country"],
        "weather": data.get("current_weather", {})
    }

# =========================
# 🌍 LIST CITIES (FILTER + SEARCH)
# =========================
@app.get("/api/cities")
def cities(
    country: str = Query(None),
    search: str = Query(None)
):
    result = CITIES

    if country:
        result = {k:v for k,v in result.items() if v["country"].lower() == country.lower()}

    if search:
        result = {k:v for k,v in result.items() if search.lower() in k.lower()}

    return result

# =========================
# ❤️ HEALTH
# =========================
@app.get("/api/health")
def health():
    return {"status": "ok"}