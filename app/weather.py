import os
import httpx
import json
import time
from typing import Dict, Any, Tuple
from dotenv import load_dotenv

# Charger la clé OpenWeather depuis .env
load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Génère une clé de cache (par tranche de 10 min)
def _cache_key(lat: float, lon: float) -> str:
    latr, lonr = round(lat, 2), round(lon, 2)
    bucket = int(time.time() // (10 * 60))
    return f"wx:{latr}:{lonr}:{bucket}"

# Géocodage : transforme une ville en (lat, lon)
async def geocode_city(city: str) -> Tuple[float, float]:
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={OPENWEATHER_API_KEY}"
    async with httpx.AsyncClient(timeout=8.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()
    if not data:
        raise ValueError(f"Ville '{city}' introuvable")
    return data[0]["lat"], data[0]["lon"]

# Récupère la météo temps réel (avec cache Redis 10 min)
async def fetch_weather(lat: float, lon: float, rds=None) -> Dict[str, Any]:
    key = _cache_key(lat, lon)
    if rds:
        cached = rds.get(key)
        if cached:
            return json.loads(cached)

    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&lang=fr"
    )
    async with httpx.AsyncClient(timeout=8.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()

    if rds:
        rds.setex(key, 600, json.dumps(data))  # expire dans 10 min

    return data

# Analyse la météo : pluie, orage, neige
def is_raining_from_payload(payload: Dict[str, Any]) -> Tuple[bool, str]:
    wid = payload["weather"][0]["id"]
    desc = payload["weather"][0]["description"]

    # Orage (200–299), Pluie (300–599), Neige (600–699)
    if 200 <= wid < 300:
        return True, f"Orage détecté (id={wid}, desc={desc})"
    elif 300 <= wid < 600:
        return True, f"Pluie détectée (id={wid}, desc={desc})"
    elif 600 <= wid < 700:
        return True, f"Neige détectée (id={wid}, desc={desc})"

    return False, f"Aucune pluie/neige/orage (id={wid}, desc={desc})"
