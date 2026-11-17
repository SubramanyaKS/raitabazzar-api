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

    def test_weather_endpoint_with_mocked_open_meteo(self):
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
        self.assertEqual(data["source"], "Open-Meteo (Live)")
        self.assertTrue(data["is_live"])
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
        self.assertEqual(data["condition"], "Rain")
        self.assertTrue(data.get("is_live"))
        self.assertIn("Postpone pesticide spraying", data["advisory_en"])
        self.assertIn("ಕೀಟನಾಶಕ ಸಿಂಪಡಣೆಯನ್ನು ಮುಂದೂಡಿ", data["advisory_kn"])

    def test_weather_fallback_to_wttr_when_open_meteo_fails(self):
        # Open-Meteo throws error, wttr.in succeeds
        def get_mock(url, **kwargs):
            if "open-meteo.com" in url:
                raise Exception("Render 429 Rate Limit on Open-Meteo")
            elif "wttr.in" in url:
                mock_resp = MagicMock()
                mock_resp.status_code = 200
                mock_resp.json.return_value = {
                    "current_condition": [
                        {
                            "temp_C": "26.0",
                            "humidity": "58",
                            "windspeedKmph": "9.5",
                            "weatherDesc": [{"value": "Sunny"}],
                        }
                    ]
                }
                return mock_resp
            raise ValueError("Unknown URL")

        mock_http_client = MagicMock()
        mock_http_client.__aenter__ = AsyncMock(return_value=mock_http_client)
        mock_http_client.__aexit__ = AsyncMock(return_value=None)
        mock_http_client.get = AsyncMock(side_effect=get_mock)

        with patch.object(weather_services.httpx, "AsyncClient", return_value=mock_http_client):
            response = self.client.get("/api/v1/weather?district=Mysuru")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["district"], "Mysuru")
        self.assertEqual(data["temperature_c"], 26.0)
        self.assertEqual(data["condition"], "Sunny")
        self.assertEqual(data["source"], "wttr.in (Live)")
        self.assertTrue(data["is_live"])

    def test_weather_endpoint_fallback_when_both_fail(self):
        mock_http_client = MagicMock()
        mock_http_client.__aenter__ = AsyncMock(return_value=mock_http_client)
        mock_http_client.__aexit__ = AsyncMock(return_value=None)
        mock_http_client.get = AsyncMock(side_effect=Exception("Total network outage"))

        with patch.object(weather_services.httpx, "AsyncClient", return_value=mock_http_client):
            response = self.client.get("/api/v1/weather?district=Bangalore")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["district"], "Bangalore Urban")
        self.assertEqual(data["temperature_c"], 22.0)
        self.assertFalse(data["is_live"])
        self.assertIn("Normal seasonal conditions across Karnataka", data["advisory_en"])

    async def test_weather_service_direct_call_with_lat_lon(self):
        data = await weather_services.get_weather_data(lat=12.52, lon=76.89, force_refresh=True)
        self.assertTrue(data["success"])
        self.assertIn("district", data)
        self.assertIn("temperature_c", data)
        self.assertIn("advisory_en", data)
