from fastapi import FastAPI
import psutil
import requests

app = FastAPI(title="DevNet Monitoring System")

# =========================
# 🌤️ WEATHER FUNCTION
# =========================
def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        return requests.get(url).json()
    except:
        return {"error": "weather api failed"}

# =========================
# 🖥️ SYSTEM
# =========================
@app.get("/api/system")
def system_info():
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory()._asdict(),
        "disk": psutil.disk_usage("/")._asdict()
    }

# =========================
# 🌊 SOUSSE
# =========================
@app.get("/api/weather/sousse")
def weather_sousse():
    return get_weather(35.8256, 10.6411)

# =========================
# 🕌 KAIROUAN
# =========================
@app.get("/api/weather/kairouan")
def weather_kairouan():
    return get_weather(35.6781, 10.0963)

# =========================
# ❤️ HEALTH
# =========================
@app.get("/api/health")
def health():
    return {"status": "ok"}