from sqlalchemy import Column, String, DateTime, Numeric, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class OHLCV(Base):
    __tablename__ = 'ohlcv'

    id = Column(String(36), primary_key=True)
    symbol = Column(String(10), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    open = Column(Numeric(12, 4))
    high = Column(Numeric(12, 4))
    low = Column(Numeric(12, 4))
    close = Column(Numeric(12, 4))
    volume = Column(Numeric(16, 2))

    __table_args__ = (
        UniqueConstraint('symbol', 'timestamp', name='uq_symbol_timestamp'),
    )

    def __repr__(self):
        return f"<OHLCV(symbol={self.symbol}, date={self.timestamp}, close={self.close})>"