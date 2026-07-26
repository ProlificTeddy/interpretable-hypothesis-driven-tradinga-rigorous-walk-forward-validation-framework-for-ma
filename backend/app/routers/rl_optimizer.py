from fastapi import APIRouter, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from ..models.hypothesis import Hypothesis
from ..models.ohlcv import OHLCV
from ..models.rl import RLTrainingResult
from ..schemas.rl import RLTrainingRequest, RLTrainingResultResponse
from ..services.rl_optimizer_service import RLStrategyOptimizer
from ..database import get_db
import uuid

router = APIRouter(prefix="/api/rl-optimizer", tags=["rl-optimizer"])

@router.post("/train", response_model=RLTrainingResultResponse)
async def train_rl_strategy(
    request: RLTrainingRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    hypothesis = db.query(Hypothesis).filter(Hypothesis.id == request.hypothesis_id).first()
    if not hypothesis:
        raise HTTPException(status_code=404, detail="Hypothesis not found")
    
    training_id = str(uuid.uuid4())
    optimizer = RLStrategyOptimizer(
        db=db,
        hypothesis=hypothesis,
        training_id=request.training_id,
        risk_free_rate=request.risk_free_rate,
    )
    
    background_tasks.add_task(optimizer.run_training)
    
    return {
        "training_id": training_id,
        "status": "pending",
        "start_time": datetime.utcnow()
    }

@router.get("/results/{training_id}", response_model=RLTrainingResultResponse)
def get_training_results(training_id: str, db: Session = Depends(get_db)):
    result = db.query(RLTrainingResult).filter(RLTrainingResult.id == training_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Training result not found")
    return result