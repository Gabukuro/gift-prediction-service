import unittest
from unittest.mock import patch 
from src.models.product import Product
from src.services.product import ProductService

class TestProductService(unittest.TestCase):
    
  def test_parse_categories_from_detected_objects(self):
    categories = ProductService().parse_categories_from_detected_objects([{ "name": "bicycle", "quantity": 3 }])
    self.assertEqual(categories, {"sports & fitness": { "quantity" : 3 }})

    categories = ProductService().parse_categories_from_detected_objects([{ "name": "suitcase", "quantity": 3 }])
    self.assertEqual(categories, {"accessories": { "quantity" : 3 }, "bags & luggage": { "quantity" : 3 }})

  @patch('src.services.product.ProductRepository.get_products_by_categories')
  def test_filter_products(self, get_products_by_categories):
    mock_products = [
      Product("product1", "sports & fitness", "", "", "",  5.0, 100),
      Product("product2", "sports & fitness", "", "", "", 4.7, 100),
      Product("product3", "bags & luggage", "", "", "", 4.4, 100),
      Product("product4", "bags & luggage", "", "", "", 4.1, 100),
      Product("product5", "bags & luggage", "", "", "", 4.2, 100),
    ]
    get_products_by_categories.return_value = mock_products

    products = ProductService().filter_products([
      {"name": "suitcase", "quantity": 3},
      {"name": "bicycle", "quantity": 15}
    ])

    self.assertEqual(len(products), 3)
