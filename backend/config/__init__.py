from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    WALKFORWARD_WINDOW: int = 252
    MAX_HYPOTHESIS_COMPLEXITY: float = 0.85
    RISK_FREE_RATE: float = 0.02

    class Config:
        env_file = ".env"

settings = Settings()