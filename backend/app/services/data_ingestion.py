import yfinance as yf
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from typing import List
from ..models.ohlcv import OHLCV
import logging

logger = logging.getLogger(__name__)

class DataIngestionService:
    def __init__(self, db: Session, symbols: List[str]):
        self.db = db
        self.symbols = symbols

    def _preprocess_data(self, df: pd.DataFrame, symbol: str) -> pd.DataFrame:
        df = df.reset_index()
        df['Symbol'] = symbol
        df.rename(columns={
            'Date': 'timestamp',
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        }, inplace=True)
        df['timestamp'] = df['timestamp'].dt.tz_convert('UTC')
        return df[['timestamp', 'Symbol', 'open', 'high', 'low', 'close', 'volume']]

    def _batch_insert(self, data: pd.DataFrame):
        try:
            records = data.to_dict('records')
            self.db.bulk_insert_mappings(OHLCV, [{
                'symbol': r['Symbol'],
                'timestamp': r['timestamp'],
                'open': r['open'],
                'high': r['high'],
                'low': r['low'],
                'close': r['close'],
                'volume': r['volume']
            } for r in records])
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Batch insert failed: {str(e)}")
            raise

    def ingest(self, start_date: str = '2015-01-01', end_date: str =2024-12-31'):
        for symbol in self.symbols:
            try:
                logger.info(f"Fetching data for {symbol}")
                data = yf.download(
                    symbol,
                    start=start_date,
                    end=end_date,
                    progress=False,
                    group_by='ticker'
                )
                if data.empty:
                    continue

                processed = self._preprocess_data(data, symbol)
                self._batch_insert(processed)
                logger.info(f"Successfully ingested {len(processed)} records for {symbol}")

            except Exception as e:
                logger.error(f"Failed to ingest data for {symbol}: {str(e)}")
                continue