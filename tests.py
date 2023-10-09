#!/usr/bin/env python3

import unittest
from unittest.mock import MagicMock
# import analysis functions
from app import analysis_functions
from app import Artpieces

class TestExample(unittest.TestCase):
    def setUp(self):
        self.AnalysisFunctions = analysis_functions()

    def test_get_iif(self):
        test_id = "some_id"
        expected = f"https://www.artic.edu/iiif/2/{test_id}/full/843,/0/default.jpg"
    
        self.assertEqual(self.AnalysisFunctions.get_iif(test_id), expected)

    def test_volume_calculator(self):
        test_details = {
                    "depth_cm": 2,
                    "depth_in": 2,
                    "width_cm": 2,
                    "width_in": 2,
                    "height_cm": 2,
                    "height_in": 2,
                    "diameter_cm": 0,
                    "diameter_in": 0,
                    "clarification": "test part"
                }
        
        test_details_1 = {
                    "depth_cm": 0,
                    "depth_in": 0,
                    "width_cm": 2,
                    "width_in": 2,
                    "height_cm": 2,
                    "height_in": 2,
                    "diameter_cm": 0,
                    "diameter_in": 0,
                    "clarification": "test part"
                }
        
        self.assertEqual(self.AnalysisFunctions.get_volume_string(test_details), "8")
        self.assertEqual(self.AnalysisFunctions.get_volume_string(test_details_1), "0")

    def test_area_calculator(self):
        test_details = {
                    "depth_cm": 0,
                    "depth_in": 0,
                    "width_cm": 2,
                    "width_in": 2,
                    "height_cm": 2,
                    "height_in": 2,
                    "diameter_cm": 0,
                    "diameter_in": 0,
                    "clarification": "test part"
                }
        self.assertEqual(self.AnalysisFunctions.get_area_string(test_details), "4")

    def test_json_generator(self):
        test_artpieces = [
            Artpieces(id=1, name="piece1"),
            Artpieces(id=2, name="piece2"),
            Artpieces(id=3, name="piece3")
        ]
        self.AnalysisFunctions.get_iif = MagicMock(return_value="http://some-link")
        self.AnalysisFunctions.get_dimensions_detail = MagicMock(return_value="some physical description of the artwork")
        expected = '''[{"id": 1, "name": "piece1", "image_link": "http://some-link", "dimensions_detail": "some physical description of the artwork"}, {"id": 2, "name": "piece2", "image_link": "http://some-link", "dimensions_detail": "some physical description of the artwork"}, {"id": 3, "name": "piece3", "image_link": "http://some-link", "dimensions_detail": "some physical description of the artwork"}]'''

        self.assertEqual(self.AnalysisFunctions.ArtpiecesJson(test_artpieces),expected)
if __name__ == "__main__":
    unittest.main()
    
