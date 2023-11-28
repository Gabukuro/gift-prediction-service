from src import db
from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import UUID

class PredictionProduct(db.Model):
    __tablename__ = 'prediction_products'

    prediction_id = db.Column(UUID(as_uuid=True))
    product_id = db.Column(UUID(as_uuid=True))
    rank_position = db.Column(db.Integer)

    __table_args__ = (
        db.PrimaryKeyConstraint('prediction_id', 'product_id'),
    )

    def __init__(self, prediction_id, product_id, rank_position):
        self.prediction_id = prediction_id
        self.product_id = product_id
        self.rank_position = rank_position

    def to_dict(self):
      return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


