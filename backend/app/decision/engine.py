from __future__ import annotations

import logging
from typing import Optional, Tuple

from app.core.config import get_settings
from app.decision import ml_engine, rules_engine
from app.schemas import RecommendationRequest, RecommendationResponse

logger = logging.getLogger(__name__)


def recommend(req: RecommendationRequest) -> RecommendationResponse:
    """
    Decision system orchestration:
    1) Mandatory rule-based recommendation.
    2) Optional ML recommendation that can override based on confidence.
    """
    rules_resp = rules_engine.recommend_with_rules(req)
    settings = get_settings()

    if not settings.ml_enabled:
        return rules_resp

    # ML is optional and must gracefully fail.
    try:
        confidence_threshold = settings.ml_confidence_threshold
        resolved_path = ml_engine.resolve_ml_model_path(settings.ml_model_path)  # type: ignore[attr-defined]
    except Exception:
        resolved_path = None

    try:
        settings = get_settings()
        resolved_path = ml_engine.resolve_ml_model_path(settings.ml_model_path)  # type: ignore[attr-defined]
        model_exists = resolved_path is not None and ml_engine.is_model_available(resolved_path)
    except Exception:
        model_exists = False
        resolved_path = None

    if not model_exists:
        if settings.ml_auto_train:
            try:
                model_path = ml_engine.train_default_model_if_missing()
                model_exists = bool(model_path)
            except Exception:
                logger.exception("ML auto-train failed; falling back to rules.")
                model_exists = False

    if not model_exists:
        return rules_resp

    try:
        ml_alg, ml_conf = ml_engine.predict_best_algorithm(req)
        if ml_conf >= settings.ml_confidence_threshold:
            # Override recommendation with ML suggestion.
            return rules_engine.recommend_with_overridden_algorithm(
                req=req,
                recommended_algorithm=ml_alg,
                decision_layer="ensemble",
                model_used=True,
                ml_confidence=ml_conf,
            )

        return rules_resp
    except Exception:
        logger.exception("ML prediction failed; falling back to rules.")
        return rules_resp

