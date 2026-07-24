from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends
from ..services.data_ingestion import DataIngestionService
from ..models.ohlcv import OHLCV
from ..database import get_db

router = APIRouter(prefix="/api/data", tags=["data-ingestion"])

@router.post("/ingest")
async def ingest_historical_data(
    symbols: List[str],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    try:
        service = DataIngestionService(db, symbols)
        background_tasks.add_task(service.ingest)
        return {"message": "Data ingestion started in background"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initiate data ingestion: {str(e)}"
        )