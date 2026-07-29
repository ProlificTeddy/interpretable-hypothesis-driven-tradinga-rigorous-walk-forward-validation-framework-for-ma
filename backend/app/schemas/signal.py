from pydantic import BaseModel
from datetime import datetime
from typing import Dict, List, Optional

class SignalResponse(BaseModel):
    timestamp: datetime
    symbol: str
    value: bool
    confidence: Optional[Dict[str, float]]

class SignalValidationRequest(BaseModel):
    hypothesis_id: str
    validation_data: List[dict]
    metrics: List[str] = ['accuracy', 'precision', 'recall']

class SignalValidationResponse(BaseModel):
    hypothesis_id: str
    metrics: Dict[str, float]
    confusion_matrix: Dict[str, int]
    sample_size: int
    validation_window: Dict[str, datetime]