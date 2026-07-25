import pandas as pd
from sqlalchemy.orm import Session
from typing import Dict
from ..models.hypothesis import Hypothesis, Signal
from ..models.ohlcv import OHLCV
from ..database import get_db
import logging

logger = logging.getLogger(__name__)

class SignalGenerator:
    def __init__(self, db: Session, hypothesis: Hypothesis):
        self.db = db
        self.hypothesis = hypothesis
        self.params = hypothesis.parameters

    def _calculate_volume_spike(self, df: pd.DataFrame) -> pd.Series:
        window = self.params.get('window_size', 20)
        multiplier = self.params.get('multiplier', 2.5)
        df['volume_ma'] = df['volume'].rolling(window=window).mean()
        return (df['volume'] > (multiplier * df['volume_ma']))

    def generate(self):
        try:
            symbols = self.params.get('symbols', [])
            for symbol in symbols:
                # Fetch OHLCV data
                data = self.db.query(OHLCV).filter(
                    OHLCV.symbol == symbol
                ).order_by(OHLCV.timestamp).all()

                df = pd.DataFrame([{
                    'timestamp': r.timestamp,
                    'volume': float(r.volume)
                } for r in data])

                if df.empty:
                    continue

                # Apply hypothesis-specific logic
                if self.hypothesis.name == 'Volume Spike Detection':
                    signals = self._calculate_volume_spike(df)
                else:
                    raise NotImplementedError("Hypothesis type not supported")

                # Store signals
                for idx, val in signals.iteritems():
                    signal = Signal(
                        hypothesis_id=self.hypothesis.id,
                        timestamp=df.iloc[idx]['timestamp'],
                        symbol=symbol,
                        value=bool(val),
                        features={
                            'volume': df.iloc[idx]['volume'],
                            'volume_ma': df.iloc[idx].get('volume_ma', None)
                        }
                    )
                    self.db.add(signal)

            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Signal generation failed: {str(e)}")
            raise