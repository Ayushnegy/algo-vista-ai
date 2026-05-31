from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.benchmark import router as benchmark_router
from app.api.recommend import router as recommend_router
from app.api.train_ml import router as train_ml_router
from app.api.export import router as export_router


def create_app() -> FastAPI:
    app = FastAPI(title="AlgoVista AI - Adaptive Algorithm Recommendation System", version="0.1.0")

    # Light-frontend dev server integration.
   origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    async def health() -> dict:
        return {"status": "ok"}

    app.include_router(recommend_router)
    app.include_router(benchmark_router)
    app.include_router(train_ml_router)
    app.include_router(export_router)
    return app


app = create_app()

