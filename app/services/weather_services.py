from datetime import datetime, timedelta, timezone
import logging
import time
from typing import Any, Dict, Optional

import httpx

from app.data.data import DISTRICT_COORDINATES

logger = logging.getLogger(__name__)

_weather_cache: Dict[str, Dict[str, Any]] = {}
CACHE_TTL_SECONDS = 3600  # 1 hour cache
IST = timezone(timedelta(hours=5, minutes=30))

WMO_WEATHER_CODES = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing Rime Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Dense Drizzle",
    61: "Slight Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    71: "Slight Snow Fall",
    80: "Slight Rain Showers",
    81: "Moderate Rain Showers",
    82: "Violent Rain Showers",
    95: "Thunderstorm",
    96: "Thunderstorm with Slight Hail",
    99: "Thunderstorm with Heavy Hail",
}


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


def _generate_advisory(rain_prob: float, weather_code: int) -> Dict[str, str]:
    if rain_prob > 50 or weather_code in {61, 63, 65, 80, 81, 82, 95, 96, 99}:
        return {
            "condition": "Rain Expected" if rain_prob > 50 else WMO_WEATHER_CODES.get(weather_code, "Rainy"),
            "advisory_en": "High chance of rain. Postpone pesticide spraying and secure harvested produce.",
            "advisory_kn": "ಮಳೆಯ ಸಾಧ್ಯತೆ ಹೆಚ್ಚಿದೆ. ಕೀಟನಾಶಕ ಸಿಂಪಡಣೆಯನ್ನು ಮುಂದೂಡಿ ಮತ್ತು ಕಟಾವು ಮಾಡಿದ ಬೆಳೆಯನ್ನು ರಕ್ಷಿಸಿ.",
        }
    elif rain_prob > 25:
        return {
            "condition": WMO_WEATHER_CODES.get(weather_code, "Partly Cloudy"),
            "advisory_en": "Moderate chance of rain. Monitor harvest drying and plan field irrigation accordingly.",
            "advisory_kn": "ಸಾಧಾರಣ ಮಳೆಯ ಸಾಧ್ಯತೆ. ಕಟಾವು ಒಣಗಿಸುವಿಕೆಯನ್ನು ಗಮನಿಸಿ ಮತ್ತು ನೀರಾವರಿಯನ್ನು ಯೋಜಿಸಿ.",
        }
    else:
        return {
            "condition": WMO_WEATHER_CODES.get(weather_code, "Clear / Sunny"),
            "advisory_en": "Dry and favorable weather. Ideal for harvesting, drying grains, and spraying.",
            "advisory_kn": "ಒಣ ಹವೆ ಮತ್ತು ಅನುಕೂಲಕರ ವಾತಾವರಣ. ಕಟಾವು, ಧಾನ್ಯ ಒಣಗಿಸಲು ಮತ್ತು ಸಿಂಪಡಣೆಗೆ ಸೂಕ್ತವಾಗಿದೆ.",
        }


async def get_weather_data(
    district: Optional[str] = "Mandya",
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    force_refresh: bool = False,
) -> Dict[str, Any]:
    """
    Fetches live weather data from Open-Meteo for Karnataka districts or coordinates.
    Cached for CACHE_TTL_SECONDS to avoid upstream rate limits.
    """
    coords = _resolve_coordinates(district=district, lat=lat, lon=lon)
    cache_key = f"{round(coords['lat'], 2)}_{round(coords['lon'], 2)}"
    current_time = time.time()
    min_refresh_interval = 30  # seconds anti-DoS cooldown

    if cache_key in _weather_cache:
        cached = _weather_cache[cache_key]
        time_since_cached = current_time - cached["cached_at"]
        if not force_refresh and time_since_cached < CACHE_TTL_SECONDS:
            return cached["data"]
        # If force_refresh is requested too frequently, serve cached data to prevent DoS
        if force_refresh and time_since_cached < min_refresh_interval:
            return cached["data"]

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={coords['lat']}&longitude={coords['lon']}"
        f"&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
        f"&daily=precipitation_probability_max"
        f"&timezone=Asia%2FKolkata"
    )

    headers = {
        "User-Agent": "RaitaBazzar/1.0 (Agriculture Advisory)",
        "Accept": "application/json",
    }

    try:
        async with httpx.AsyncClient(headers=headers, timeout=httpx.Timeout(6.0, connect=3.0)) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()

        curr = data.get("current", {})
        daily = data.get("daily", {})
        rain_prob_list = daily.get("precipitation_probability_max", [])
        rain_prob = float(rain_prob_list[0]) if rain_prob_list else 10.0
        temp = float(curr.get("temperature_2m", 28.0))
        humidity = int(curr.get("relative_humidity_2m", 65))
        wind = float(curr.get("wind_speed_10m", 12.0))
        code = int(curr.get("weather_code", 1))

        advisory_info = _generate_advisory(rain_prob=rain_prob, weather_code=code)

        result = {
            "success": True,
            "district": coords["name"],
            "temperature_c": round(temp, 1),
            "condition": advisory_info["condition"],
            "weather_code": code,
            "humidity_pct": humidity,
            "wind_speed_kmh": round(wind, 1),
            "rain_chance_pct": int(rain_prob),
            "advisory_en": advisory_info["advisory_en"],
            "advisory_kn": advisory_info["advisory_kn"],
            "updated_at": datetime.now(IST).isoformat(),
        }

        _weather_cache[cache_key] = {"cached_at": current_time, "data": result}
        return result

    except Exception as exc:
        logger.warning("Open-Meteo weather fetch failed (%s); returning baseline advisory", type(exc).__name__)
        return {
            "success": True,
            "district": coords["name"],
            "temperature_c": 28.0,
            "condition": "Partly Cloudy",
            "weather_code": 2,
            "humidity_pct": 65,
            "wind_speed_kmh": 12.0,
            "rain_chance_pct": 10,
            "advisory_en": "Normal seasonal conditions. Suitable for standard farming activities.",
            "advisory_kn": "ಸಾಮಾನ್ಯ ಹವಾಮಾನ. ಕೃಷಿ ಚಟುವಟಿಕೆಗಳಿಗೆ ಸೂಕ್ತವಾಗಿದೆ.",
            "updated_at": datetime.now(IST).isoformat(),
        }
