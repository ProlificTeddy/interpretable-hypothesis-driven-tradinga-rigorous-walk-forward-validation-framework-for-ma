import pandas as pd
import numpy as np
from typing import Dict

class BacktestingService:
    def run_backtest(self, data: pd.DataFrame, signals: pd.DataFrame) -> Dict[str, float]:
        merged = pd.merge(data, signals, on=['timestamp', 'symbol'], suffixes=('', '_signal'))
        merged['position'] = merged['signal'].astype(int).diff().fillna(0)
        
        # Calculate returns
        merged['strategy_returns'] = merged['position'].shift(1) * merged['close'].pct_change()
        merged['cumulative_returns'] = (1 + merged['strategy_returns']).cumprod()
        
        # Risk metrics
        sharpe = self._annualized_sharpe(merged['strategy_returns'])
        max_dd = self._max_drawdown(merged['cumulative_returns'])
        sortino = self._sortino_ratio(merged['strategy_returns'])
        
        return {
            'sharpe_ratio': sharpe,
            'max_drawdown': max_dd,
            'sortino_ratio': sortino,
            'total_return': merged['cumulative_returns'].iloc[-1] - 1,
            'win_rate': (merged['strategy_returns'] > 0).mean()
        }
    
    def _annualized_sharpe(self, returns: pd.Series) -> float:
        if len(returns) < 2 or returns.std() == 0:
            return 0.0
        return (returns.mean() * 252) / (returns.std() * np.sqrt(252))
    
    def _max_drawdown(self, cumulative: pd.Series) -> float:
        peak = cumulative.expanding(min_periods=1).max()
        trough = cumulative.expanding(min_periods=1).min()
        return (trough / peak - 1).min()
    
    def _sortino_ratio(self, returns: pd.Series) -> float:
        downside = returns[returns < 0]
        if len(downside) < 2 or downside.std() == 0:
            return 0.0
        return (returns.mean() * 252) / (downside.std() * np.sqrt(252))