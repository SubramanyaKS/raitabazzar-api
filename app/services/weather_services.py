import logging
import time
from typing import Any, Dict, Optional

import httpx

from app.data.data import DISTRICT_COORDINATES

logger = logging.getLogger(__name__)

_weather_cache: Dict[str, Dict[str, Any]] = {}
CACHE_TTL = 3600  # 1 hour cache


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

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": coords["lat"],
        "longitude": coords["lon"],
        "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
        "daily": "precipitation_probability_max",
        "timezone": "Asia/Kolkata",
    }

    try:
        # Increased timeout to 15s to allow for Render network latency
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()

        curr = data.get("current", {})
        daily = data.get("daily", {})
        rain_prob = daily.get("precipitation_probability_max", [0])[0]
        temp = curr.get("temperature_2m", 20.0)
        humidity = curr.get("relative_humidity_2m", 60)
        wind = curr.get("wind_speed_10m", 10.0)
        code = curr.get("weather_code", 1)

        # Map Open-Meteo weather codes
        if code in [0, 1]:
            condition = "Clear / Sunny"
        elif code in [2, 3]:
            condition = "Partly Cloudy"
        elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
            condition = "Rain"
        else:
            condition = "Overcast"

        if rain_prob > 50:
            advisory_en = "High chance of rain. Postpone pesticide spraying and secure harvested produce."
            advisory_kn = "ಮಳೆಯ ಸಾಧ್ಯತೆ ಹೆಚ್ಚಿದೆ. ಕೀಟನಾಶಕ ಸಿಂಪಡಣೆಯನ್ನು ಮುಂದೂಡಿ ಮತ್ತು ಕಟಾವು ಮಾಡಿದ ಬೆಳೆಯನ್ನು ರಕ್ಷಿಸಿ."
        else:
            advisory_en = "Dry and favorable weather. Ideal for harvesting, drying grains, and spraying."
            advisory_kn = "ಒಣ ಹವೆ ಮತ್ತು ಅನುಕೂಲಕರ ವಾತಾವರಣ. ಕಟಾವು, ಧಾನ್ಯ ಒಣಗಿಸಲು ಮತ್ತು ಸಿಂಪಡಣೆಗೆ ಸೂಕ್ತವಾಗಿದೆ."

        result = {
            "success": True,
            "district": coords["name"],
            "temperature_c": temp,
            "humidity_pct": humidity,
            "wind_speed_kmh": wind,
            "rain_chance_pct": rain_prob,
            "condition": condition,
            "weather_code": code,
            "advisory_en": advisory_en,
            "advisory_kn": advisory_kn,
            "is_live": True,
        }

        _weather_cache[cache_key] = {"cached_at": current_time, "data": result}
        return result

    except Exception as e:
        logger.error(f"Open-Meteo fetch failed for {district}: {e}")
        print(f"Weather error on Render: {e}")
        return {
            "success": True,
            "district": coords["name"],
            "temperature_c": 28.0,
            "humidity_pct": 65,
            "wind_speed_kmh": 12.0,
            "rain_chance_pct": 10,
            "condition": "Partly Cloudy",
            "advisory_en": "Normal seasonal conditions. Suitable for standard farming activities.",
            "advisory_kn": "ಸಾಮಾನ್ಯ ಹವಾಮಾನ. ಕೃಷಿ ಚಟುವಟಿಕೆಗಳಿಗೆ ಸೂಕ್ತವಾಗಿದೆ.",
            "error_detail": str(e),  # Helps debug directly in JSON
            "is_live": False,
        }
