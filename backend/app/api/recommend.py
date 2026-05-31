from __future__ import annotations

import logging
from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from app.db.mongo import get_mongo_store
from app.decision.engine import recommend as recommend_engine
from app.schemas import RecommendationRequest, RecommendationResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/recommend", response_model=RecommendationResponse)
async def recommend_endpoint(payload: RecommendationRequest) -> RecommendationResponse:
    try:
        response = recommend_engine(payload)

        # Persist query + recommendation (best-effort).
        mongo = get_mongo_store()
        mongo.save_user_query(payload.model_dump())
        mongo.save_recommendation(
            {
                "request": payload.model_dump(),
                "response": response.model_dump(),
            }
        )

        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Recommendation failed.")
        raise HTTPException(status_code=500, detail=str(e))

