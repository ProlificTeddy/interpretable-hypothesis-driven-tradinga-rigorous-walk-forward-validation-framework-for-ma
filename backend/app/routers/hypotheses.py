from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..models.hypothesis import Hypothesis
from ..schemas.hypothesis import HypothesisCreate
from ..database import get_db

router = APIRouter(prefix="/api/hypotheses", tags=["hypotheses"])

@router.post("/", response_model=HypothesisCreate)
def create_hypothesis(hypothesis: HypothesisCreate, db: Session = Depends(get_db)):
    try:
        db_hypothesis = Hypothesis(**hypothesis.dict())
        db.add(db_hypothesis)
        db.commit()
        db.refresh(db_hypothesis)
        return db_hypothesis
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[HypothesisCreate])
def list_hypotheses(db: Session = Depends(get_db)):
    return db.query(Hypothesis).order_by(Hypothesis.created_at.desc()).all()