from __future__ import annotations

import math
import os
import random
from dataclasses import dataclass
from typing import Callable, Dict, Optional, Tuple

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer

from app.core.config import get_settings, resolve_ml_model_path
from app.decision import rules_engine
from app.schemas import GraphType, MemoryLevel, ProblemType, RecommendationRequest


ModelArtifact = Dict[str, object]


def _feature_dict(req: RecommendationRequest) -> Dict[str, object]:
    return {
        "problem_type": req.problem_type,
        "memory": req.memory,
        "recursive_allowed": int(req.recursive_allowed),
        "nearly_sorted": int(req.nearly_sorted),
        "input_size_log": math.log10(req.input_size + 1),
        "graph_type": req.graph_type or "none",
    }


def _random_request(rng: random.Random) -> RecommendationRequest:
    problem_type = rng.choice(["sorting", "searching", "graph", "dp"])  # type: ignore[list-item]
    input_size = int(10 ** rng.uniform(1.0, 5.0))  # log-uniform between ~1e1 and 1e5
    nearly_sorted = rng.choice([True, False])
    memory = rng.choice(["low", "medium", "high"])  # type: ignore[list-item]
    recursive_allowed = rng.choice([True, False])
    graph_type: Optional[GraphType] = None
    if problem_type == "graph":
        graph_type = rng.choice(["dense", "sparse"])  # type: ignore[list-item]

    return RecommendationRequest(
        problem_type=problem_type,  # type: ignore[arg-type]
        input_size=input_size,
        nearly_sorted=nearly_sorted,
        memory=memory,  # type: ignore[arg-type]
        recursive_allowed=recursive_allowed,
        graph_type=graph_type,
    )


def train_synthetic_model(
    oracle_fn: Callable[[RecommendationRequest], str],
    model_path: str,
    n_samples: int = 6000,
    random_seed: int = 42,
) -> str:
    """
    Train a classifier on synthetic (feature -> best-algorithm) pairs.
    The oracle is the rule-based engine, ensuring label quality.
    """
    rng = random.Random(random_seed)

    X_dicts = []
    y = []
    for _ in range(n_samples):
        req = _random_request(rng)
        best = oracle_fn(req)
        X_dicts.append(_feature_dict(req))
        y.append(best)

    vectorizer = DictVectorizer(sparse=False)
    X = vectorizer.fit_transform(X_dicts)

    clf = RandomForestClassifier(
        n_estimators=350,
        max_depth=None,
        random_state=random_seed,
        n_jobs=-1,
    )
    clf.fit(X, y)

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    artifact: ModelArtifact = {"vectorizer": vectorizer, "clf": clf}
    joblib.dump(artifact, model_path)
    return model_path


_artifact_cache: Optional[ModelArtifact] = None


def _load_artifact(model_path: str) -> ModelArtifact:
    global _artifact_cache
    if _artifact_cache is not None:
        return _artifact_cache
    artifact = joblib.load(model_path)
    _artifact_cache = artifact
    return artifact


def is_model_available(model_path: str) -> bool:
    return os.path.exists(model_path)


def predict_best_algorithm(req: RecommendationRequest) -> Tuple[str, float]:
    """
    Returns: (predicted_algorithm_name, confidence_in_[0..1])
    """
    settings = get_settings()
    resolved = resolve_ml_model_path(settings.ml_model_path)
    if not resolved:
        raise FileNotFoundError("ML model artifact not found.")
    artifact = _load_artifact(resolved)
    vectorizer: DictVectorizer = artifact["vectorizer"]  # type: ignore[assignment]
    clf: RandomForestClassifier = artifact["clf"]  # type: ignore[assignment]

    Xv = vectorizer.transform([_feature_dict(req)])
    probs = clf.predict_proba(Xv)[0]
    best_idx = int(np.argmax(probs))
    confidence = float(probs[best_idx])
    predicted = str(clf.classes_[best_idx])
    return predicted, confidence


def train_default_model_if_missing() -> Optional[str]:
    settings = get_settings()
    resolved = resolve_ml_model_path(settings.ml_model_path)
    if resolved and os.path.exists(resolved):
        return None

    # If model isn't present, we train using rules as oracle.
    model_path = resolved or settings.ml_model_path

    def oracle(req: RecommendationRequest) -> str:
        resp = rules_engine.recommend_with_rules(req)
        return resp.recommended_algorithm

    n_samples = 8000
    return train_synthetic_model(
        oracle_fn=oracle,
        model_path=model_path,
        n_samples=n_samples,
        random_seed=42,
    )

