import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class Settings(BaseModel):
    app_name: str = Field(default="AlgoVista AI - AARS")
    environment: str = Field(default=os.getenv("ENVIRONMENT", "development"))

    mongo_uri: str = Field(default=os.getenv("MONGO_URI", "mongodb://localhost:27017"))
    mongo_db: str = Field(default=os.getenv("MONGO_DB", "algovista_ai"))

    # ML is optional. If model artifact is missing, we fall back to rules-only.
    ml_enabled: bool = Field(
        default=os.getenv("ML_ENABLED", "true").lower() in {"1", "true", "yes"},
    )
    ml_auto_train: bool = Field(
        default=os.getenv("ML_AUTO_TRAIN", "false").lower() in {"1", "true", "yes"},
    )
    ml_model_path: str = Field(
        default=os.getenv("ML_MODEL_PATH", "models/model.joblib"),
    )
    ml_confidence_threshold: float = Field(
        default=float(os.getenv("ML_CONFIDENCE_THRESHOLD", "0.55")),
        ge=0.0,
        le=1.0,
    )

    # Safety caps to keep benchmarking fast and deterministic.
    max_benchmark_input_size: int = Field(
        default=int(os.getenv("MAX_BENCHMARK_INPUT_SIZE", "2500")),
        ge=50,
        le=50000,
    )
    benchmark_sample_counts: int = Field(
        default=int(os.getenv("BENCHMARK_SAMPLE_COUNTS", "3")),
        ge=1,
        le=20,
    )


def get_settings() -> Settings:
    return Settings()


def resolve_ml_model_path(ml_model_path: str) -> Optional[str]:
    # Supports both absolute and relative paths from repo root.
    if os.path.isabs(ml_model_path) and os.path.exists(ml_model_path):
        return ml_model_path
    if os.path.exists(ml_model_path):
        return ml_model_path
    # Try resolving relative to repo root.
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    candidate = os.path.join(repo_root, ml_model_path)
    if os.path.exists(candidate):
        return candidate
    return None

