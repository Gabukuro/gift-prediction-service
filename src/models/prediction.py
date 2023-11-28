from src import db
from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import UUID
import uuid
from enum import Enum

class PredictionStatusEnum(Enum):
    pending = 'pending'
    completed = 'completed'
    failed = 'failed'

class Prediction(db.Model):
    __tablename__ = 'predictions'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    username = db.Column(db.String(100))
    feedback_rate = db.Column(db.Integer)
    status = db.Column(db.Enum(PredictionStatusEnum), default=PredictionStatusEnum.pending)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def to_dict(self):
      return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


