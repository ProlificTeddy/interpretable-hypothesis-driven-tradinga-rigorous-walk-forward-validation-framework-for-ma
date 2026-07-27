from sqlalchemy import Column, DateTime, String, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WalkForwardResult(Base):
    __tablename__ = 'walk_forward_results'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    hypothesis_id = Column(UUID(as_uuid=True), ForeignKey('hypotheses.id'), nullable=False)
    in_sample_start = Column(DateTime(timezone=True), nullable=False)
    in_sample_end = Column(DateTime(timezone=True), nullable=False)
    out_of_sample_start = Column(DateTime(timezone=True), nullable=False)
    out_of_sample_end = Column(DateTime(timezone=True), nullable=False)
    parameters = Column(JSON, nullable=False)
    training_metrics = Column(JSON, nullable=False)
    testing_metrics = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())