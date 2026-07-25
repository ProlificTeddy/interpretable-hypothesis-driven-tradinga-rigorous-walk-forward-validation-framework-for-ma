from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..models.hypothesis import Hypothesis, Signal
from ..services.signal_generation_service import SignalGenerator
from ..database import get_db

router = APIRouter(prefix="/api/signals", tags=["signals"])

@router.post("/generate/{hypothesis_id}")
def generate_signals(hypothesis_id: str, db: Session = Depends(get_db)):
    hypothesis = db.query(Hypothesis).filter(Hypothesis.id == hypothesis_id).first()
    if not hypothesis:
        raise HTTPException(status_code=404, detail="Hypothesis not found")
    
    try:
        generator = SignalGenerator(db, hypothesis)
        generator.generate()
        return {"status": "success", "message": "Signal generation completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{hypothesis_id}", response_model=List[dict])
def get_signals(hypothesis_id: str, db: Session = Depends(get_db)):
    signals = db.query(Signal).filter(Signal.hypothesis_id == hypothesis_id).all()
    return [{
        "timestamp": s.timestamp,
        "symbol": s.symbol,
        "value": s.value,
        "features": s.features
    } for s in signals]