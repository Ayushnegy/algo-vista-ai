from __future__ import annotations

import os
from typing import Optional

from fastapi import APIRouter, HTTPException

from app.core.config import get_settings
from app.decision import ml_engine, rules_engine
from app.schemas import RecommendationRequest

router = APIRouter()


@router.post("/train-ml")
async def train_ml(n_samples: int = 8000) -> dict:
    settings = get_settings()
    model_path = ml_engine.resolve_ml_model_path(settings.ml_model_path) or settings.ml_model_path

    def oracle(req: RecommendationRequest) -> str:
        resp = rules_engine.recommend_with_rules(req)
        return resp.recommended_algorithm

    try:
        trained_path = ml_engine.train_synthetic_model(
            oracle_fn=oracle,
            model_path=model_path,
            n_samples=n_samples,
            random_seed=42,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"model_path": trained_path, "samples": n_samples}

