from ultralytics import YOLO
from PIL import Image
from io import BytesIO
from collections import defaultdict
from src.services.product import ProductService
import instaloader
import requests

class AnalysisService:
    def __init__(self):
      """
      This class doesn't require any initialization logic at the moment,
      so the __init__ method is left empty.
      """
      pass

    def analyze_profile(self, username):
      images = self.retrieve_images_from_instagram(username)
      objects = []

      print("images count:", len(images))
      for image in images:
        objects.append(self.detect_objects_on_image(image))
      
      try:
        filtered_products = ProductService().filter_products(self.group_and_count_objects(objects))
        return filtered_products
      except Exception as e:
        print(e)
        return []
    
    def group_and_count_objects(self, objects):

      count = defaultdict(int)
      for subarray in objects:
        for obj in subarray:
          count[obj] += 1
  
      return [{ "name": object, "quantity": quantity } for object, quantity in count.items()]

    def retrieve_images_from_instagram(self, username):
      L = instaloader.Instaloader()
      posts = instaloader.Profile.from_username(L.context, username).get_posts()
      urls = []
      for post in posts:
         urls.append(post.url)
      return urls
    
    def detect_objects_on_image(self, src):
      model = YOLO("yolov8n.pt")
      image = Image.open(BytesIO(requests.get(src).content))
      results = model.predict(image)
      result = results[0]
      objects = []
      for box  in result.boxes:
        class_id = box.cls[0].item()
        objects.append(result.names[class_id])

      return objects
