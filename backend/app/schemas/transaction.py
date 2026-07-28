from pydantic import BaseModel, Field
from typing import Optional

class TransactionCost(BaseModel):
    fee_per_trade: float = Field(0.0, ge=0, description="Fixed fee per trade in USD")
    fee_per_share: float = Field(0.0, ge=0, description="Variable fee per share traded")
    slippage_percent: float = Field(0.0, ge=0, le=1, description="Slippage as percentage of trade value")
    tax_rate: float = Field(0.0, ge=0, le=1, description="Capital gains tax rate")

class PositionConstraints(BaseModel):
    max_position_size: float = Field(float('inf'), gt=0, description="Maximum allowed position size in units")
    max_leverage: float = Field(1.0, gt=0, description="Maximum allowed leverage ratio")
    allow_short: bool = Field(False, description="Whether short positions are permitted")