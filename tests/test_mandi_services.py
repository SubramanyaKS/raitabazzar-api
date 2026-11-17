import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
from fastapi import HTTPException

from app.routers import mandi
from app.services import mandi_services


class MandiRatesTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.cached_rates_patch = patch.object(mandi_services, "_cached_merged_rates", [])
        self.cache_times_patch = patch.object(mandi_services, "_last_fetch_time", 0)
        self.api_key_patch = patch.object(
            mandi_services.settings, "DATAGOV_API_KEY", "test-api-key"
        )
        self.cached_rates_patch.start()
        self.cache_times_patch.start()
        self.api_key_patch.start()

    def tearDown(self):
        self.api_key_patch.stop()
        self.cache_times_patch.stop()
        self.cached_rates_patch.stop()

    async def test_district_filter_and_benchmark_fallback(self):
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {
            "records": [
                {"district": "Koppal", "commodity": "Tomato", "modal_price": "1000", "min_price": "900", "max_price": "1100"},
            ]
        }
        client = MagicMock()
        client.__aenter__ = AsyncMock(return_value=client)
        client.__aexit__ = AsyncMock(return_value=None)
        client.get = AsyncMock(return_value=response)

        with patch.object(mandi_services.httpx, "AsyncClient", return_value=client):
            koppal_rates = await mandi_services.fetch_karnataka_mandi_rates(
                district="Koppal", force_refresh=True
            )

        self.assertTrue(all(rate["district"] == "Koppal" for rate in koppal_rates))
        self.assertTrue(any(rate["commodity"] == "Tomato" for rate in koppal_rates))

    async def test_upstream_failure_falls_back_to_benchmarks(self):
        client = MagicMock()
        client.__aenter__ = AsyncMock(return_value=client)
        client.__aexit__ = AsyncMock(return_value=None)
        client.get = AsyncMock(side_effect=httpx.ReadTimeout("upstream timeout"))

        with patch.object(mandi_services.httpx, "AsyncClient", return_value=client):
            rates = await mandi_services.fetch_karnataka_mandi_rates(
                district="Mandya", force_refresh=True
            )
            self.assertTrue(len(rates) > 0)
            self.assertTrue(all(rate["district"] == "Mandya" for rate in rates))

    async def test_route_returns_503_when_mandi_data_is_unavailable(self):
        unavailable = AsyncMock(
            side_effect=mandi_services.MandiDataUnavailableError("feed unavailable")
        )
        with patch.object(mandi, "fetch_karnataka_mandi_rates", unavailable):
            with self.assertRaises(HTTPException) as raised:
                await mandi.get_mandi_rates(
                    district="Koppal",
                    commodity=None,
                    refresh=False,
                )

        self.assertEqual(raised.exception.status_code, 503)
