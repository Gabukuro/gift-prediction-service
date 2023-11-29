from src.repositories.product import ProductRepository
import pandas as pd

class ProductService:
  def __init__(self):
    self.coco_categories_relation = [
        { "name": "women's clothing", "objects": ["handbag"] },
        {
          "name": "sports & fitness",
          "objects": [
            "bicycle",
            "baseball bat",
            "baseball glove",
            "skateboard",
            "surfboard",
            "tennis racket",
            "sports ball",
            "snowboard",
            "skis",
            "frisbee",
          ],
        },
        { "name": "industrial supplies", "objects": ["scissors"] },
        { "name": "toys & baby products", "objects": ["kite", "teddy bear"] },
        {
          "name": "beauty & health",
          "objects": ["hair drier", "toothbrush", "person"],
        },
        { "name": "accessories", "objects": ["umbrella", "suitcase"] },
        { "name": "men's clothing", "objects": ["tie"] },
        {
          "name": "appliances",
          "objects": ["microwave", "oven", "toaster", "refrigerator", "clock"],
        },
        {
          "name": "home & kitchen",
          "objects": [
            "bottle",
            "wine glass",
            "cup",
            "fork",
            "knife",
            "spoon",
            "bowl",
            "bench",
            "diningtable",
            "cake",
            "sandwich",
            "sink",
          ],
        },
        { "name": "women's shoes", "objects": ["handbag"] },
        { "name": "bags & luggage", "objects": ["handbag", "backpack", "suitcase"] },
        {
          "name": "home, kitchen, pets",
          "objects": [
            "pottedplant",
            "bench",
            "chair",
            "sofa",
            "bed",
            "diningtable",
            "vase",
          ],
        },
        { "name": "car & motorbike", "objects": ["car", "motorbike", "aeroplane"] },
        {
          "name": "tv, audio & cameras",
          "objects": ["cell phone", "mouse", "laptop", "tvmonitor"],
        },
        {
          "name": "pet supplies",
          "objects": ["bird", "cat", "dog", "horse", "sheep", "cow"],
        },
        { "name": "men's shoes", "objects": ["tie"] },
        {
          "name": "grocery & gourmet foods",
          "objects": [
            "banana",
            "apple",
            "orange",
            "broccoli",
            "carrot",
            "hot dog",
            "pizza",
            "donut",
          ],
        },
      ]

  def parse_categories_from_detected_objects(self, detected_objects):
    categories_count = {}

    for object in detected_objects:
      for category in self.coco_categories_relation:
        if object["name"] in category["objects"]:
          if category["name"] not in categories_count:
            categories_count[category["name"]] = { "quantity": object["quantity"] }
          else:
            categories_count[category["name"]]["quantity"] += object["quantity"]

    return categories_count
  
  def filter_products(self, detected_objects):
    categories = self.parse_categories_from_detected_objects(detected_objects)

    sorted_categories = sorted(categories.items(), key=lambda x: x[1]['quantity'], reverse=True)
    top_categories = sorted_categories[:3]
    top_category_names = [category[0] for category in top_categories]

    products = ProductRepository().get_products_by_categories(top_category_names)
    df_products = pd.DataFrame([product.to_dict() for product in products])

    df_products['ratings_weight'] = df_products['ratings'] * df_products['no_of_ratings']
    df_products['category_weight'] = df_products['main_category'].map(lambda x: next((quantity_dict['quantity'] for category, quantity_dict in top_categories if category == x), 0))

    df_products_sorted = df_products.sort_values(by=['category_weight', 'ratings_weight'], ascending=[False, False])

    return df_products_sorted.head(3)



