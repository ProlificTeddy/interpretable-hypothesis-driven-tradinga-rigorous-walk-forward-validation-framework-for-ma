import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from typing import Dict, Any
from ..models.ohlcv import OHLCV
from ..models.walk_forward import WalkForwardResult
from ..services.rl_optimizer_service import RLStrategyOptimizer
from ..services.signal_generation_service import SignalGenerator
from ..services.backtesting_service import BacktestingService
import logging
import uuid
import isodate

logger = logging.getLogger(__name__)

class WalkForwardValidator:
    def __init__(self, db: Session, hypothesis, request):
        self.db = db
        self.hypothesis = hypothesis
        self.request = request
        self.validation_id = uuid.uuid4()
        self.symbols = self._get_hypothesis_symbols()
        self.full_data = self._load_data()
        self.backtester = BacktestingService()
        self.date_format = "%Y-%m-%dT%H:%M:%SZ"
    
    def _parse_duration(self, duration_str: str) -> relativedelta:
        return isodate.parse_duration(duration_str)
    
    def _get_hypothesis_symbols(self):
        return self.hypothesis.parameters.get('symbols', ['AAPL'])
    
    def _load_data(self):
        query = self.db.query(OHLCV).filter(OHLCV.symbol.in_(self.symbols))
        df = pd.read_sql(query.statement, self.db.bind)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df.sort_values('timestamp').set_index('timestamp')
    
    def _generate_windows(self):
        in_sample_delta = self._parse_duration(self.request.in_sample_window)
        out_of_sample_delta = self._parse_duration(self.request.out_of_sample_window)
        step_delta = self._parse_duration(self.request.step_size)
        
        windows = []
        current_start = self.full_data.index.min().to_pydatetime()
        end_date = self.full_data.index.max().to_pydatetime()
        
        for _ in range(self.request.number_of_periods):
            in_sample_end = current_start + in_sample_delta
            out_of_sample_end = in_sample_end + out_of_sample_delta
            
            if out_of_sample_end > end_date:
                break
            
            windows.append({
                'in_sample': (current_start, in_sample_end),
                'out_of_sample': (in_sample_end, out_of_sample_end)
            })
            
            current_start += step_delta
        
        return windows
    
    def execute_validation(self):
        windows = self._generate_windows()
        
        for period, window in enumerate(windows, 1):
            logger.info(f"Processing validation period {period}/{len(windows)}")
            
            # In-sample phase
            in_sample_data = self.full_data.loc[window['in_sample'][0]:window['in_sample'][1]]
            
            # RL Optimization
            rl_optimizer = RLStrategyOptimizer(self.db, self.hypothesis)
            training_result = rl_optimizer.train(in_sample_data)
            
            # Signal Generation
            signal_generator = SignalGenerator(self.db, self.hypothesis)
            signal_generator.params = training_result.optimized_parameters
            signals = signal_generator.generate(in_sample_data.reset_index())
            
            # Backtesting
            training_metrics = self.backtester.run_backtest(in_sample_data.reset_index(), signals)
            
            # Out-of-sample testing
            oos_data = self.full_data.loc[window['out_of_sample'][0]:window['out_of_sample'][1]]
            oos_signals = signal_generator.generate(oos_data.reset_index())
            testing_metrics = self.backtester.run_backtest(oos_data.reset_index(), oos_signals)
            
            # Save results
            result = WalkForwardResult(
                hypothesis_id=self.hypothesis.id,
                in_sample_start=window['in_sample'][0],
                in_sample_end=window['in_sample'][1],
                out_of_sample_start=window['out_of_sample'][0],
                out_of_sample_end=window['out_of_sample'][1],
                parameters=training_result.optimized_parameters,
                training_metrics=training_metrics,
                testing_metrics=testing_metrics
            )
            self.db.add(result)
        
        self.db.commit()