from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict
from .transaction import TransactionCost, PositionConstraints

class WalkForwardRequest(BaseModel):
    hypothesis_id: str
    number_of_periods: int = Field(34, ge=1, le=100)
    in_sample_window: str = Field(..., description="ISO duration format e.g. 'P1Y2M10D'")
    out_of_sample_window: str = Field(..., description="ISO duration format e.g. 'P3M'")
    step_size: str = Field(..., description="Rolling window step size e.g. 'P1M'")
    transaction_cost: TransactionCost = Field(default_factory=TransactionCost)
    position_constraints: PositionConstraints = Field(default_factory=PositionConstraints)

class WalkForwardPeriodResult(BaseModel):
    period: int
    in_sample_start: datetime
    in_sample_end: datetime
    out_of_sample_start: datetime
    out_of_sample_end: datetime
    performance: Dict[str, float]
    risk_metrics: Dict[str, float]
    transaction_costs: float

class WalkForwardResponse(BaseModel):
    hypothesis_id: str
    results: List[WalkForwardPeriodResult]
    consensus_metrics: Dict[str, float]
    stability_ratio: float