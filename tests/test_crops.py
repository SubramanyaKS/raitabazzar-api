import unittest
from fastapi.testclient import TestClient
from app.main import app


class CropsApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_search_crop_in_kannada_script(self):
        response = self.client.get("/api/v1/crops/search?q=ಈರುಳ್ಳಿ&district=Mandya")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["query"], "ಈರುಳ್ಳಿ")
        matched = data["matched_crop"]
        self.assertEqual(matched["standard_name"], "Onion")
        self.assertEqual(matched["kannada_name"], "ಈರುಳ್ಳಿ")
        self.assertEqual(matched["hindi_name"], "प्याज")
        self.assertEqual(matched["category"], "Vegetables")
        self.assertIn("ಈರುಳ್ಳಿ", matched["synonyms_matched"])
        self.assertIsNotNone(matched["benchmark"])
        self.assertEqual(matched["benchmark"]["district"], "Bangalore")
        self.assertEqual(matched["benchmark"]["market"], "Yeshwanthpur APMC")
        self.assertEqual(matched["benchmark"]["modal_price"], 34.0)

    def test_search_crop_with_specific_district_benchmark(self):
        response = self.client.get("/api/v1/crops/search?q=Tomato&district=Mandya")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        matched = data["matched_crop"]
        self.assertEqual(matched["standard_name"], "Tomato")
        self.assertEqual(matched["benchmark"]["district"], "Mandya")
        self.assertEqual(matched["benchmark"]["market"], "Mandya APMC")
        self.assertEqual(matched["benchmark"]["modal_price"], 22.0)

    def test_search_crop_with_kanglish_transliteration(self):
        response = self.client.get("/api/v1/crops/search?q=eerulli")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["matched_crop"]["standard_name"], "Onion")

    def test_search_crop_with_hindi_transliteration(self):
        response = self.client.get("/api/v1/crops/search?q=pyaz")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["matched_crop"]["standard_name"], "Onion")

    def test_search_crop_not_found(self):
        response = self.client.get("/api/v1/crops/search?q=unknown_crop_xyz")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertIsNone(data["matched_crop"])
        self.assertIn("No matching Karnataka crop found", data["message"])

    def test_get_master_crops(self):
        response = self.client.get("/api/v1/crops/master")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertGreaterEqual(data["total"], 27)

    def test_get_master_crops_filter_category(self):
        response = self.client.get("/api/v1/crops/master?category=Vegetables")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        for crop in data["crops"]:
            self.assertEqual(crop["category"].lower(), "vegetables")
