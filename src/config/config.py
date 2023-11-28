import os
import boto3

class Config:
  def __init__(self):
    self.ENV = os.getenv('ENV', 'development')
    self.DEBUG = os.getenv('DEBUG', True)
    self.PORT = os.getenv('PORT', 3000)
    self.HOST = os.getenv('HOST', '0.0.0.0')
    self.AWS_URL = os.getenv('AWS_URL', 'http://localhost:4566')
    self.AWS_REGION = os.getenv('AWS_REGION', 'us-east-2')
    self.SQS_QUEUE_NAME = os.getenv('SQS_QUEUE_NAME', 'profile-analysis-queue')
    self.SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql+psycopg2://postgres:postgres@localhost:5432/insta-gift-api')


