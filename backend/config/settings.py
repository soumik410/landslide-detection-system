"""
Centralized configuration for the landslide monitoring backend.
Reads from environment variables (.env) with sensible local defaults.
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # --- App ---
    APP_NAME: str = "Landslide Early-Warning System"
    ENV: str = "development"
    DEBUG: bool = True

    # --- Database ---
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'landslide.db'}"

    # --- Hardware / Serial ---
    SERIAL_PORT: str = "COM3"          # e.g. "/dev/ttyUSB0" on Linux, "COM3" on Windows
    SERIAL_BAUDRATE: int = 9600
    SERIAL_TIMEOUT: float = 1.0
    SIMULATE_HARDWARE: bool = True     # if True, generates synthetic sensor data instead of reading a real port
    POLL_INTERVAL_SECONDS: float = 2.0

    # --- LLM (Anthropic) ---
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    LLM_MODEL: str = "claude-sonnet-4-6"
    LLM_MAX_TOKENS: int = 600

    # --- Embeddings (local) ---
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    VECTOR_DB_PATH: str = str(BASE_DIR / "rag" / "vector_store.pkl")
    KNOWLEDGE_BASE_DIR: str = str(BASE_DIR / "knowledge_base")

    # --- Risk thresholds (used by risk/rules.py) ---
    MOISTURE_HIGH_PCT: float = 70.0
    RAIN_HIGH_MM_PER_HR: float = 20.0
    TILT_HIGH_DEGREES: float = 5.0
    DISPLACEMENT_HIGH_CM: float = 3.0

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()