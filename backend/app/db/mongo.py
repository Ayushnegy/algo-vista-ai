import datetime as dt
import logging
from typing import Any, Dict, Optional

from pymongo import MongoClient

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class MongoStore:
    def __init__(self) -> None:
        settings = get_settings()
        self._client = MongoClient(settings.mongo_uri)
        self._db = self._client[settings.mongo_db]

    def save_recommendation(self, payload: Dict[str, Any]) -> None:
        try:
            payload = {**payload, "created_at": dt.datetime.utcnow()}
            self._db["recommendations"].insert_one(payload)
        except Exception:
            # Recommendation should never fail because Mongo is down.
            logger.exception("Failed to save recommendation to Mongo.")

    def save_benchmark_log(self, payload: Dict[str, Any]) -> None:
        try:
            payload = {**payload, "created_at": dt.datetime.utcnow()}
            self._db["performance_logs"].insert_one(payload)
        except Exception:
            logger.exception("Failed to save benchmark log to Mongo.")

    def save_user_query(self, payload: Dict[str, Any]) -> None:
        try:
            payload = {**payload, "created_at": dt.datetime.utcnow()}
            self._db["user_queries"].insert_one(payload)
        except Exception:
            logger.exception("Failed to save user query to Mongo.")


_store: Optional[MongoStore] = None


def get_mongo_store() -> MongoStore:
    global _store
    if _store is None:
        _store = MongoStore()
    return _store

