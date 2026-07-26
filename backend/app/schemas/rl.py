from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any

class RLTrainingRequest(BaseModel):
    hypothesis_id: str
    training_id: Optional[str] = None
    risk_free_rate: float = 0.02
    max_episodes: int = 100
    
class RLTrainingResultResponse(BaseModel):
    training_id: str
    status: str
    start_time: datetime
    end_time: Optional[datetime]
    training_metrics: Dict[str, Any]
    optimized_parameters: Dict[str, float]