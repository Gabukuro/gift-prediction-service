import boto3
import json
import time
from src import app, db
from src.config.config import Config
from src.services.analysis import AnalysisService
from src.models.prediction import Prediction, PredictionStatusEnum
from src.models.prediction_product import PredictionProduct
from concurrent.futures import ThreadPoolExecutor


class Consumer:
  def __init__(self):
    config = Config()
    self.sqs = boto3.resource("sqs", endpoint_url=config.AWS_URL, region_name=config.AWS_REGION)
    self.queue = self.sqs.Queue("profile-analysis-queue")
    self.executor = ThreadPoolExecutor(max_workers=1)

  
  def listen(self):
    while True:
      try:
        messages = self.queue.receive_messages(
          MaxNumberOfMessages=1,
          WaitTimeSeconds=20
        )
        for message in messages:
          self.executor.submit(self.process_message, message)

      except Exception as e:
        print(e)
        continue

      time.sleep(5)

  def process_message(self, message):
    with app.app_context():
      body = json.loads(message.body)
      print("Processing message:", body["id"])

      payload = body["payload"]
      print("Payload: ", payload)

      prediction = Prediction.query.filter_by(username=payload["username"], status=PredictionStatusEnum.pending).first()

      if prediction is not None:
        try:
          prediction.status = "processing"
          db.session.commit()

          products = AnalysisService().analyze_profile(payload["username"])
          rank = 1

          for product in products.itertuples():
            new_prediction_product = PredictionProduct(prediction_id=prediction.id, product_id=product.id, rank_position=rank)
            db.session.add(new_prediction_product)
            rank += 1

          prediction.status = "completed"
        except Exception as e:
          print("error: ", e)
          prediction.status = "failed"

        finally:
          db.session.commit()
          message.delete()
          print("Message processed:", body["id"])

