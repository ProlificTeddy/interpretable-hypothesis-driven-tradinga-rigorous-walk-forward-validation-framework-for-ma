from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

Base = declarative_base()

class RLTrainingResult(Base):
    __tablename__ = 'rl_training_results'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    hypothesis_id = Column(UUID(as_uuid=True), ForeignKey('hypotheses.id'), nullable=False)
    parameters = Column(JSON, nullable=False)
    training_metrics = Column(JSON, nullable=False)
    optimized_parameters = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())