from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings
from .routers import data_ingestion

# Hypothesis lifecycle management
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize validation engine
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    app.state.db = SessionLocal()
    yield
    # Cleanup after validation cycles
    app.state.db.close()

app = FastAPI(
    title="Hypothesis-Driven Trading Validator",
    description="Robust framework for financial strategy validation",
    lifespan=lifespan
)

app.include_router(data_ingestion.router)

@app.get("/")
async def health_check():
    return {"status": "operational", "validation_system": "active"}