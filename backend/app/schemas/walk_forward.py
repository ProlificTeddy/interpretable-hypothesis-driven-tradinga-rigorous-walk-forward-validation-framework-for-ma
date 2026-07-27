from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict

class WalkForwardRequest(BaseModel):
    hypothesis_id: str
    number_of_periods: int = Field(34, ge=1, le=100)
    in_sample_window: str = Field(..., description="ISO duration format e.g. 'P1Y2M10D'")
    out_of_sample_window: str = Field(..., description="ISO duration format e.g. 'P3M'")
    step_size: str = Field(..., description="Rolling window step size e.g. 'P1M'")

class WalkForwardPeriodResult(BaseModel):
    period: int
    in_sample_start: datetime
    in_sample_end: datetime
    out_of_sample_start: datetime
    out_of_sample_end: datetime
    parameters: Dict[str, float]
    training_metrics: Dict[str, float]
    testing_metrics: Dict[str, float]

class WalkForwardResponse(BaseModel):
    validation_id: str
    hypothesis_id: str
    total_periods: int
    results: List[WalkForwardPeriodResult]
    created_at: datetime