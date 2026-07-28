import pandas as pd
import numpy as np
from typing import Dict
from ..schemas.transaction import TransactionCost, PositionConstraints

class BacktestingService:
    def run_backtest(self, data: pd.DataFrame, signals: pd.DataFrame, 
                   transaction_cost: TransactionCost, position_constraints: PositionConstraints) -> Dict[str, float]:
        merged = pd.merge(data, signals, on=['timestamp', 'symbol'], suffixes=('', '_signal'))
        
        # Position calculation with constraints
        merged['position'] = merged['signal'].astype(int)
        
        if not position_constraints.allow_short:
            merged['position'] = merged['position'].clip(lower=0)
        merged['position'] = merged['position'].clip(upper=position_constraints.max_position_size)
        
        # Calculate position changes and transaction costs
        merged['trade'] = merged['position'].diff().fillna(0)
        merged['fixed_fee'] = (merged['trade'] != 0).astype(int) * transaction_cost.fee_per_trade
        merged['variable_fee'] = abs(merged['trade']) * transaction_cost.fee_per_share
        merged['slippage'] = abs(merged['trade']) * merged['close'] * transaction_cost.slippage_percent
        total_costs = merged['fixed_fee'] + merged['variable_fee'] + merged['slippage']
        
        # Calculate returns with cost adjustment
        merged['strategy_returns'] = (
            merged['position'].shift(1) * merged['close'].pct_change()
        ) - (total_costs / merged['close'].shift(1)).fillna(0)
        
        # Leverage constraint enforcement
        merged['exposure'] = merged['position'] * merged['close']
        merged['exposure'] = merged['exposure'].clip(upper=position_constraints.max_leverage * merged['exposure'].mean())
        
        merged['cumulative_returns'] = (1 + merged['strategy_returns']).cumprod()
        
        # Risk metrics
        max_drawdown = (merged['cumulative_returns'].cummax() - merged['cumulative_returns']).max()
        sharpe_ratio = merged['strategy_returns'].mean() / merged['strategy_returns'].std() * np.sqrt(252)
        
        return {
            "total_return": merged['cumulative_returns'].iloc[-1] - 1,
            "max_drawdown": max_drawdown,
            "sharpe_ratio": sharpe_ratio,
            "turnover": merged['trade'].abs().sum(),
            "total_costs": total_costs.sum()
        }