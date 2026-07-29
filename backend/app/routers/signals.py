from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..models.hypothesis import Hypothesis, Signal
from ..schemas.signal import SignalResponse, SignalValidationRequest, SignalValidationResponse
from ..services.signal_generation_service import SignalGenerator
from ..database import get_db

router = APIRouter(prefix="/api/signals", tags=["signals"])

@router.post("/generate/{hypothesis_id}", response_model=List[SignalResponse])
def generate_signals(hypothesis_id: str, db: Session = Depends(get_db)):
    hypothesis = db.query(Hypothesis).filter(Hypothesis.id == hypothesis_id).first()
    if not hypothesis:
        raise HTTPException(status_code=404, detail="Hypothesis not found")
    
    try:
        generator = SignalGenerator(db)
        signals = generator.generate(hypothesis)
        return [SignalResponse(
            timestamp=s.timestamp,
            symbol=s.symbol,
            value=s.value,
            confidence=s.confidence
        ) for s in signals]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{hypothesis_id}", response_model=List[SignalResponse])
def get_signals(
    hypothesis_id: str,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Signal).filter(Signal.hypothesis_id == hypothesis_id)
    
    if start:
        query = query.filter(Signal.timestamp >= start)
    if end:
        query = query.filter(Signal.timestamp <= end)
        
    signals = query.all()
    return [SignalResponse(
        timestamp=s.timestamp,
        symbol=s.symbol,
        value=s.value,
        confidence=s.confidence
    ) for s in signals]

@router.post("/validate", response_model=SignalValidationResponse)
def validate_signals(
    request: SignalValidationRequest,
    db: Session = Depends(get_db)
):
    hypothesis = db.query(Hypothesis).filter(Hypothesis.id == request.hypothesis_id).first()
    if not hypothesis:
        raise HTTPException(status_code=404, detail="Hypothesis not found")
    
    try:
        generator = SignalGenerator(db)
        validation = generator.validate(
            hypothesis=hypothesis,
            validation_data=request.validation_data,
            metrics=request.metrics
        )
        return SignalValidationResponse(**validation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))