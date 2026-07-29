from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Optional
from .hypothesis import HypothesisCreate
from .walk_forward import WalkForwardResponse
from .rl import RLTrainingResultResponse

class ValidationStatisticsResponse(BaseModel):
    hypothesis_id: str
    total_walk_forwards: int
    success_rate: float
    average_profit: float
    max_drawdown: float
    sharpe_ratio: float
    sortino_ratio: float
    risk_adjusted_return: float
    last_updated: datetime

class PerformanceMetricsResponse(BaseModel):
    walk_forward_id: str
    hypothesis_id: str
    in_sample_performance: Dict[str, float]
    out_of_sample_performance: Dict[str, float]
    risk_metrics: Dict[str, float]
    transaction_cost_impact: Dict[str, float]

class HypothesisSummaryResponse(BaseModel):
    hypothesis: HypothesisCreate
    latest_walk_forward: WalkForwardResponse
    best_rl_training: RLTrainingResultResponse
    signal_effectiveness: Dict[str, float]
    risk_assessment: Dict[str, float]