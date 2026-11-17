import logging
import time
from typing import Any, Dict, List, Optional

import httpx

from app.config import settings
from app.data.data import KARNATAKA_DISTRICT_BENCHMARKS

logger = logging.getLogger(__name__)

# Complete verified Karnataka district benchmarks.
# Used when an APMC has not concluded/uploaded today's auction yet (e.g. before 12:00 PM or holidays).


# Global cache for the merged dataset
_cached_merged_rates: List[Dict[str, Any]] = []
_last_fetch_time: float = 0
AGMARKNET_URL = f"https://api.data.gov.in/resource/{settings.MANDI_RESOURCE_ID}"


class MandiDataUnavailableError(RuntimeError):
    pass


async def fetch_karnataka_mandi_rates(
    district: Optional[str] = None,
    commodity: Optional[str] = None,
    force_refresh: bool = False,
) -> List[Dict[str, Any]]:
    global _cached_merged_rates, _last_fetch_time

    current_time = time.time()
    time_since_last_fetch = current_time - _last_fetch_time
    cache_expired = (
        not _cached_merged_rates
        or time_since_last_fetch > settings.CACHE_TTL_SECONDS
    )
    # Prevent cache-busting DoS attacks on upstream AGMARKNET
    can_force_refresh = force_refresh and (
        time_since_last_fetch >= getattr(settings, "MIN_REFRESH_INTERVAL_SECONDS", 30)
    )

    if can_force_refresh or cache_expired:
        live_records: List[Dict[str, Any]] = []
        try:
            if not settings.DATAGOV_API_KEY.strip():
                logger.warning("DATAGOV_API_KEY not set; using Karnataka benchmark data.")
            else:
                params = {
                    "api-key": settings.DATAGOV_API_KEY,
                    "format": "json",
                    "filters[state]": "Karnataka",
                    "limit": 300,
                }
                headers = {
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/124.0.0.0 Safari/537.36"
                    ),
                    "Accept": "application/json",
                }

                async with httpx.AsyncClient(
                    headers=headers,
                    timeout=httpx.Timeout(20.0, connect=5.0)
                ) as client:
                    response = await client.get(AGMARKNET_URL, params=params)

                if response.status_code == 200:
                    payload = response.json()
                    records = payload.get("records") if isinstance(payload, dict) else []
                    if isinstance(records, list):
                        for idx, record in enumerate(records):
                            if not isinstance(record, dict):
                                continue

                            raw_min = float(record.get("min_price", 0) or 0)
                            raw_max = float(record.get("max_price", 0) or 0)
                            raw_modal = float(record.get("modal_price", 0) or 0)
                            record_district = str(record.get("district") or "").title()

                            raw_market = str(record.get("market") or "").strip()
                            if raw_market.upper().endswith("APMC"):
                                market_name = f"{raw_market[:-4].strip().title()} APMC".strip()
                            elif raw_market:
                                market_name = f"{raw_market.title()} APMC"
                            else:
                                market_name = "APMC"

                            arrival_date_str = str(record.get("arrival_date") or "Today")

                            live_records.append(
                                {
                                    "id": f"gov_{record_district}_{record.get('commodity', '')}_{idx}".lower().replace(
                                        " ", "_"
                                    ),
                                    "commodity": str(record.get("commodity") or "").title(),
                                    "variety": str(record.get("variety") or "Local").title(),
                                    "market": market_name,
                                    "district": record_district,
                                    "state": "Karnataka",
                                    "min_price": round(raw_min / 100.0, 1),
                                    "max_price": round(raw_max / 100.0, 1),
                                    "modal_price": round(raw_modal / 100.0, 1),
                                    "unit": "Kg",
                                    "trend": "up" if raw_modal > raw_min else "stable",
                                    "trend_pct": 5.0 if raw_modal > raw_min else 0.0,
                                    "arrival_date": f"{arrival_date_str} (Live)",
                                    "is_live": True,
                                }
                            )
                else:
                    logger.warning("data.gov.in returned status %s", response.status_code)
        except (httpx.HTTPError, ValueError, TypeError) as exc:
            logger.warning("Mandi live refresh failed (%s); using baseline benchmarks", type(exc).__name__)

        # Build composite list: Live records have top priority.
        # Verified benchmarks fill all missing districts/commodities seamlessly.
        merged: List[Dict[str, Any]] = list(live_records)
        live_district_crops = {
            (r["district"].casefold(), r["commodity"].casefold()) for r in live_records
        }

        for idx, benchmark in enumerate(KARNATAKA_DISTRICT_BENCHMARKS):
            key = (benchmark["district"].casefold(), benchmark["commodity"].casefold())
            if key not in live_district_crops:
                merged.append(
                    {
                        "id": f"bm_{benchmark['district']}_{benchmark['commodity']}_{idx}".lower().replace(
                            " ", "_"
                        ),
                        "commodity": benchmark["commodity"],
                        "variety": benchmark["variety"],
                        "market": benchmark["market"],
                        "district": benchmark["district"],
                        "state": "Karnataka",
                        "min_price": benchmark["min_price"],
                        "max_price": benchmark["max_price"],
                        "modal_price": benchmark["modal_price"],
                        "unit": benchmark["unit"],
                        "trend": "stable",
                        "trend_pct": 0.0,
                        "arrival_date": "Prev Close (Benchmark)",
                        "is_live": False,
                    }
                )

        _cached_merged_rates = merged
        _last_fetch_time = current_time

    # Filter results by district and commodity
    results = list(_cached_merged_rates)

    district_filter = district.strip() if district and district.strip() else None
    if district_filter and district_filter.casefold() != "all":
        df_lower = district_filter.casefold()
        results = [
            r for r in results
            if df_lower in r["district"].casefold() or r["district"].casefold() in df_lower
        ]

    if commodity and commodity.strip():
        c_lower = commodity.strip().casefold()
        results = [
            r for r in results
            if c_lower in r["commodity"].casefold()
        ]

    return results
