from fastapi import FastAPI
import psutil
import requests

app = FastAPI(title="DevNet Monitoring System")

# 🌤️ API météo (Tunisie)
def get_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=36.8&longitude=10.18&current_weather=true"
    try:
        return requests.get(url).json()
    except:
        return {"error": "weather api failed"}

# 🖥️ SYSTEM MONITORING
@app.get("/api/system")
def system_info():
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory()._asdict(),
        "disk": psutil.disk_usage("/")._asdict()
    }

# 🌤️ WEATHER
@app.get("/api/weather")
def weather():
    return get_weather()

# ❤️ HEALTH CHECK
@app.get("/api/health")
def health():
    return {"status": "ok"}