from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

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
    lifespan=lifespan,
    docs_url="/quant/docs",
    redoc_url=None
)

@app.get("/health")
async def health_check():
    return {
        "status": "operational",
        "validation_constraints": {
            "max_hypothesis_complexity": settings.MAX_HYPOTHESIS_COMPLEXITY,
            "required_walkforward_windows": settings.WALKFORWARD_WINDOW
        }
    }