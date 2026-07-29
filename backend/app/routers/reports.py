from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..models.hypothesis import Hypothesis
from ..models.walk_forward import WalkForwardResult
from ..models.rl import RLTrainingResult
from ..schemas.report import (
    ValidationStatisticsResponse,
    PerformanceMetricsResponse,
    HypothesisSummaryResponse
)
from ..services.report_service import ReportService
from ..database import get_db

router = APIRouter(prefix="/api/reports", tags=["reports"])

@router.get("/validation-statistics/{hypothesis_id}", response_model=ValidationStatisticsResponse)
def get_validation_statistics(
    hypothesis_id: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    service = ReportService(db)
    try:
        return service.get_validation_stats(hypothesis_id, start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performance-metrics/{hypothesis_id}", response_model=PerformanceMetricsResponse)
def get_performance_metrics(
    hypothesis_id: str,
    walk_forward_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    service = ReportService(db)
    try:
        return service.get_performance_metrics(hypothesis_id, walk_forward_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/hypothesis-summary/{hypothesis_id}", response_model=HypothesisSummaryResponse)
def get_hypothesis_summary(hypothesis_id: str, db: Session = Depends(get_db)):
    service = ReportService(db)
    try:
        return service.get_hypothesis_summary(hypothesis_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))