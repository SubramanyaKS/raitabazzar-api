from typing import Optional

from fastapi import APIRouter, Query

from app.services import weather_services

router = APIRouter(prefix="/api/v1/weather", tags=["Weather"])


@router.get("")
async def get_weather(
    district: Optional[str] = Query("Mandya", max_length=50, description="Karnataka district name (e.g. Mandya, Kolar, Bangalore)"),
    lat: Optional[float] = Query(None, ge=-90.0, le=90.0, description="Optional latitude override"),
    lon: Optional[float] = Query(None, ge=-180.0, le=180.0, description="Optional longitude override"),
    refresh: bool = Query(False, description="Force refresh from Open-Meteo"),
):
    """
    Fetches real-time weather and agricultural advisories for Karnataka districts.
    """
    return await weather_services.get_weather_data(
        district=district,
        lat=lat,
        lon=lon,
        force_refresh=refresh,
    )
