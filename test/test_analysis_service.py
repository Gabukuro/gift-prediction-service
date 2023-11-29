import unittest
import pandas as pd
from src.services.analysis import AnalysisService

class TestAnalysisService(unittest.TestCase):

  def test_group_and_count_objects(self):
    data = [
      ["dog", "dog", "cat", "egg"],
      ["car", "bird"],
      ["ball", "toothbrush", "cat", "dog"]
    ]

    result = AnalysisService().group_and_count_objects(data)
    expected_result = [
        {"name": "dog", "quantity": 3},
        {"name": "cat", "quantity": 2},
        {"name": "egg", "quantity": 1},
        {"name": "car", "quantity": 1},
        {"name": "bird", "quantity": 1},
        {"name": "ball", "quantity": 1},
        {"name": "toothbrush", "quantity": 1}
    ]

    self.assertEqual(result, expected_result)
