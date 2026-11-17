import logging
import time
from typing import Any, Dict, Optional

import httpx

from app.data.data import DISTRICT_COORDINATES

logger = logging.getLogger(__name__)

_weather_cache: Dict[str, Dict[str, Any]] = {}
CACHE_TTL = 3600  # Cache for 1 hour


def _resolve_coordinates(
    district: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
) -> Dict[str, Any]:
    if lat is not None and lon is not None:
        closest_name = "Custom Location"
        min_dist_sq = float("inf")
        for d_key, d_info in DISTRICT_COORDINATES.items():
            dist_sq = (d_info["lat"] - lat) ** 2 + (d_info["lon"] - lon) ** 2
            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                closest_name = d_info["name"]
        return {"lat": lat, "lon": lon, "name": closest_name}

    dist_key = (district or "Mandya").strip().lower()
    return DISTRICT_COORDINATES.get(dist_key, DISTRICT_COORDINATES["mandya"])


async def _fetch_from_wttr(district_name: str, client: httpx.AsyncClient) -> Dict[str, Any]:
    """Secondary Engine: wttr.in (immune to Render 429 IP blocks)"""
    url = f"https://wttr.in/{district_name}?format=j1"
    headers = {"User-Agent": "RaitaBazzarApp/1.0"}
    resp = await client.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    curr = data["current_condition"][0]

    temp = float(curr.get("temp_C", 22.0))
    humidity = int(curr.get("humidity", 60))
    wind = float(curr.get("windspeedKmph", 8.0))
    desc = curr.get("weatherDesc", [{}])[0].get("value", "Partly Cloudy")

    return {
        "temp": temp,
        "humidity": humidity,
        "wind": wind,
        "condition": desc.strip(),
        "rain_prob": 10 if "rain" not in desc.lower() else 70,
        "source": "wttr.in (Live)",
    }


async def _fetch_from_open_meteo(coords: Dict[str, Any], client: httpx.AsyncClient) -> Dict[str, Any]:
    """Primary Engine: Open-Meteo"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": coords["lat"],
        "longitude": coords["lon"],
        "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
        "daily": "precipitation_probability_max",
        "timezone": "Asia/Kolkata",
    }
    headers = {"User-Agent": "RaitaBazzarApp/1.0 (karnataka.farmers@raitabazzar.com)"}
    resp = await client.get(url, params=params, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    curr = data.get("current", {})
    daily = data.get("daily", {})
    rain_prob = daily.get("precipitation_probability_max", [0])[0]
    code = curr.get("weather_code", 1)

    if code in [0, 1]:
        condition = "Clear / Sunny"
    elif code in [2, 3]:
        condition = "Partly Cloudy"
    elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
        condition = "Rain"
    else:
        condition = "Overcast"

    return {
        "temp": float(curr.get("temperature_2m", 22.0)),
        "humidity": int(curr.get("relative_humidity_2m", 60)),
        "wind": float(curr.get("wind_speed_10m", 8.0)),
        "condition": condition,
        "rain_prob": int(rain_prob),
        "source": "Open-Meteo (Live)",
    }


async def get_weather_data(
    district: Optional[str] = "Mandya",
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    force_refresh: bool = False,
) -> Dict[str, Any]:
    dist_key = (district or "Mandya").strip().lower()
    coords = _resolve_coordinates(district=district, lat=lat, lon=lon)
    cache_key = dist_key if (lat is None or lon is None) else f"{round(coords['lat'], 2)}_{round(coords['lon'], 2)}"

    current_time = time.time()
    min_refresh_interval = 30  # seconds anti-DoS cooldown

    if cache_key in _weather_cache:
        cached = _weather_cache[cache_key]
        time_since_cached = current_time - cached["cached_at"]
        if not force_refresh and time_since_cached < CACHE_TTL:
            return cached["data"]
        # If force_refresh is requested too frequently, serve cached data to prevent DoS
        if force_refresh and time_since_cached < min_refresh_interval:
            return cached["data"]

    parsed_weather = None

    # Step 1: Try Primary (Open-Meteo) -> Step 2: Auto fallback to Secondary (wttr.in)
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            parsed_weather = await _fetch_from_open_meteo(coords, client)
        except Exception as e_meteo:
            logger.warning(f"Open-Meteo returned error ({e_meteo}). Switching to wttr.in...")
            try:
                parsed_weather = await _fetch_from_wttr(coords["name"], client)
            except Exception as e_wttr:
                logger.error(f"Both weather providers failed: {e_wttr}")

    # Step 3: If both APIs somehow fail, use seasonal district benchmark
    if not parsed_weather:
        return {
            "success": True,
            "district": coords["name"],
            "temperature_c": 22.0,
            "humidity_pct": 60,
            "wind_speed_kmh": 8.0,
            "rain_chance_pct": 10,
            "condition": "Partly Cloudy",
            "advisory_en": "Normal seasonal conditions across Karnataka.",
            "advisory_kn": "ಸಾಮಾನ್ಯ ಹವಾಮಾನ. ಕೃಷಿ ಚಟುವಟಿಕೆಗಳಿಗೆ ಸೂಕ್ತವಾಗಿದೆ.",
            "is_live": False,
        }

    rain_prob = parsed_weather["rain_prob"]
    if rain_prob > 50:
        advisory_en = "High chance of rain. Postpone pesticide spraying and secure harvested produce."
        advisory_kn = "ಮಳೆಯ ಸಾಧ್ಯತೆ ಹೆಚ್ಚಿದೆ. ಕೀಟನಾಶಕ ಸಿಂಪಡಣೆಯನ್ನು ಮುಂದೂಡಿ ಮತ್ತು ಕಟಾವು ಮಾಡಿದ ಬೆಳೆಯನ್ನು ರಕ್ಷಿಸಿ."
    else:
        advisory_en = "Dry and favorable weather. Ideal for harvesting, drying grains, and spraying."
        advisory_kn = "ಒಣ ಹವೆ ಮತ್ತು ಅನುಕೂಲಕರ ವಾತಾವರಣ. ಕಟಾವು, ಧಾನ್ಯ ಒಣಗಿಸಲು ಮತ್ತು ಸಿಂಪಡಣೆಗೆ ಸೂಕ್ತವಾಗಿದೆ."

    result = {
        "success": True,
        "district": coords["name"],
        "temperature_c": parsed_weather["temp"],
        "humidity_pct": parsed_weather["humidity"],
        "wind_speed_kmh": parsed_weather["wind"],
        "rain_chance_pct": rain_prob,
        "condition": parsed_weather["condition"],
        "advisory_en": advisory_en,
        "advisory_kn": advisory_kn,
        "source": parsed_weather["source"],
        "is_live": True,
    }

    _weather_cache[cache_key] = {"cached_at": current_time, "data": result}
    return result
