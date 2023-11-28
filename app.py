from src import app, config
from src.services.consumer import Consumer

if __name__ == '__main__':
  consumer = Consumer()
  consumer.listen()

  app.run(host= config.HOST,
          port= config.PORT,
          debug= config.DEBUG)
