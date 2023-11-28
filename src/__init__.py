from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.config.config import Config
from dotenv import load_dotenv
from healthcheck import HealthCheck

load_dotenv()

app = Flask(__name__)

config = Config()

app.env = config.ENV
app.config.from_object(config)

db = SQLAlchemy()
db.init_app(app)

from src.routes import api
app.register_blueprint(api, url_prefix='/api')

health = HealthCheck()
app.add_url_rule('/healthcheck', 'healthcheck', view_func=lambda: health.run())
