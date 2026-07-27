from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.hypothesis import Hypothesis
from ..schemas.walk_forward import WalkForwardRequest, WalkForwardResponse
from ..services.walk_forward_validator import WalkForwardValidator
from ..database import get_db
from datetime import datetime

router = APIRouter(prefix="/api/walk-forward", tags=["walk-forward"])

@router.post("/validate", response_model=WalkForwardResponse)
async def validate_hypothesis(
    request: WalkForwardRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    hypothesis = db.query(Hypothesis).filter(Hypothesis.id == request.hypothesis_id).first()
    if not hypothesis:
        raise HTTPException(status_code=404, detail="Hypothesis not found")
    
    validator = WalkForwardValidator(db, hypothesis, request)
    background_tasks.add_task(validator.execute_validation)
    
    return {
        "validation_id": str(validator.validation_id),
        "hypothesis_id": request.hypothesis_id,
        "total_periods": request.number_of_periods,
        "results": [],
        "created_at": datetime.utcnow()
    }