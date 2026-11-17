import unittest
from app.services import crop_services


class CropServicesUnitTests(unittest.TestCase):
    def test_get_master_crops_all(self):
        crops = crop_services.get_master_crops()
        self.assertGreaterEqual(len(crops), 27)

    def test_get_master_crops_filter(self):
        crops = crop_services.get_master_crops(category="Grains")
        self.assertTrue(len(crops) > 0)
        self.assertTrue(all(c["category"].lower() == "grains" for c in crops))

    def test_search_crop_kannada(self):
        result = crop_services.search_crop("ಈರುಳ್ಳಿ", district="Bangalore")
        self.assertIsNotNone(result)
        self.assertEqual(result["standard_name"], "Onion")
        self.assertEqual(result["kannada_name"], "ಈರುಳ್ಳಿ")
        self.assertEqual(result["benchmark"]["district"], "Bangalore")

    def test_search_crop_kanglish(self):
        result = crop_services.search_crop("eerulli")
        self.assertIsNotNone(result)
        self.assertEqual(result["standard_name"], "Onion")

    def test_search_crop_not_found(self):
        result = crop_services.search_crop("non_existent_crop_test")
        self.assertIsNone(result)
