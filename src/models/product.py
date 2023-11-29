from src import db
from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    name = db.Column(db.String(100))
    main_category = db.Column(db.String(100))
    sub_category = db.Column(db.String(100))
    image = db.Column(db.String(100))
    link = db.Column(db.String(100))
    ratings = db.Column(db.Float)
    no_of_ratings = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, name, main_category, sub_category, image, link, ratings, no_of_ratings):
      self.name = name
      self.main_category = main_category
      self.sub_category = sub_category
      self.image = image
      self.link = link
      self.ratings = ratings
      self.no_of_ratings = no_of_ratings
      
    def to_dict(self):
      return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


