from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings
from .routers import data_ingestion, hypotheses, rl_optimizer, signals, walk_forward

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    app.state.db = SessionLocal()
    yield
    app.state.db.close()

app = FastAPI(
    title="Hypothesis-Driven Trading Validation Platform",
    description="Robust walk-forward validation framework for financial strategies",
    lifespan=lifespan
)

app.include_router(data_ingestion.router)
app.include_router(hypotheses.router)
app.include_router(rl_optimizer.router)
app.include_router(signals.router)
app.include_router(walk_forward.router)