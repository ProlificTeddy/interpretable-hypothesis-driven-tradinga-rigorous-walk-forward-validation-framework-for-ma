from pydantic import BaseModel, Field, validator
from typing import Optional, Dict
from datetime import datetime

class HypothesisCreate(BaseModel):
    name: str = Field(..., max_length=128)
    description: Optional[str] = Field(None, max_length=1024)
    parameters: Dict

    @validator('parameters')
    def validate_complexity(cls, v):
        if 'window_size' in v and v['window_size'] > 365:
            raise ValueError('Window size cannot exceed 1 year')
        return v

class SignalSchema(BaseModel):
    timestamp: datetime
    symbol: str
    value: bool
    confidence: Optional[Dict]
    features: Optional[Dict]

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }