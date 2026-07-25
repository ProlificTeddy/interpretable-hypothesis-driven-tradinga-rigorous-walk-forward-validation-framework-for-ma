from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

Base = declarative_base()

class Hypothesis(Base):
    __tablename__ = 'hypotheses'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    parameters = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(String(32), default='draft')

class Signal(Base):
    __tablename__ = 'signals'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    hypothesis_id = Column(UUID(as_uuid=True), ForeignKey('hypotheses.id'), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    symbol = Column(String(10), nullable=False)
    value = Column(Boolean, nullable=False)
    confidence = Column(JSON)
    features = Column(JSON)

    __table_args__ = (
        UniqueConstraint('hypothesis_id', 'timestamp', 'symbol', name='uq_signal_unique'),
    )