import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.services import weather_services


class WeatherApiTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.cache_patch = patch.dict(weather_services._weather_cache, {}, clear=True)
        self.cache_patch.start()

    def tearDown(self):
        self.cache_patch.stop()

    def test_weather_endpoint_with_mocked_upstream(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "current": {
                "temperature_2m": 29.4,
                "relative_humidity_2m": 62,
                "weather_code": 2,
                "wind_speed_10m": 11.2,
            },
            "daily": {
                "precipitation_probability_max": [15],
            },
        }

        mock_http_client = MagicMock()
        mock_http_client.__aenter__ = AsyncMock(return_value=mock_http_client)
        mock_http_client.__aexit__ = AsyncMock(return_value=None)
        mock_http_client.get = AsyncMock(return_value=mock_response)

        with patch.object(weather_services.httpx, "AsyncClient", return_value=mock_http_client):
            response = self.client.get("/api/v1/weather?district=Mandya")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["district"], "Mandya")
        self.assertEqual(data["temperature_c"], 29.4)
        self.assertEqual(data["humidity_pct"], 62)
        self.assertEqual(data["rain_chance_pct"], 15)
        self.assertIn("Dry and favorable", data["advisory_en"])
        self.assertIn("ಒಣ ಹವೆ", data["advisory_kn"])

    def test_weather_endpoint_high_rain_advisory(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "current": {
                "temperature_2m": 24.0,
                "relative_humidity_2m": 85,
                "weather_code": 63,
                "wind_speed_10m": 18.0,
            },
            "daily": {
                "precipitation_probability_max": [75],
            },
        }

        mock_http_client = MagicMock()
        mock_http_client.__aenter__ = AsyncMock(return_value=mock_http_client)
        mock_http_client.__aexit__ = AsyncMock(return_value=None)
        mock_http_client.get = AsyncMock(return_value=mock_response)

        with patch.object(weather_services.httpx, "AsyncClient", return_value=mock_http_client):
            response = self.client.get("/api/v1/weather?district=Kolar")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["district"], "Kolar")
        self.assertEqual(data["condition"], "Rain Expected")
        self.assertIn("Postpone pesticide spraying", data["advisory_en"])
        self.assertIn("ಕೀಟನಾಶಕ ಸಿಂಪಡಣೆಯನ್ನು ಮುಂದೂಡಿ", data["advisory_kn"])

    def test_weather_endpoint_fallback_on_network_failure(self):
        mock_http_client = MagicMock()
        mock_http_client.__aenter__ = AsyncMock(return_value=mock_http_client)
        mock_http_client.__aexit__ = AsyncMock(return_value=None)
        mock_http_client.get = AsyncMock(side_effect=Exception("Network error"))

        with patch.object(weather_services.httpx, "AsyncClient", return_value=mock_http_client):
            response = self.client.get("/api/v1/weather?district=Bangalore")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["district"], "Bangalore Urban")
        self.assertEqual(data["temperature_c"], 28.0)
        self.assertIn("Normal seasonal conditions", data["advisory_en"])

    async def test_weather_service_direct_call_with_lat_lon(self):
        data = await weather_services.get_weather_data(lat=12.52, lon=76.89, force_refresh=True)
        self.assertTrue(data["success"])
        self.assertIn("district", data)
        self.assertIn("temperature_c", data)
        self.assertIn("advisory_en", data)
