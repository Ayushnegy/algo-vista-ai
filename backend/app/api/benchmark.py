from __future__ import annotations

import random
import time
from typing import Callable, Dict, List

from fastapi import APIRouter, HTTPException

from app.db.mongo import get_mongo_store
from app.algorithms.sorting import heap_sort, insertion_sort, merge_sort, quick_sort
from app.algorithms.searching import binary_search, linear_search
from app.core.config import get_settings
from app.schemas import BenchmarkRequest, BenchmarkAlgorithmTiming, BenchmarkPoint, BenchmarkResponse

router = APIRouter()


def _benchmark_sizes(n: int, settings) -> List[int]:
    cap = settings.max_benchmark_input_size
    # Ensure we always benchmark at least 3 points for chart smoothness.
    pts = [max(50, n // 4), max(100, n // 2), max(200, n)]
    pts = [min(int(p), cap) for p in pts]
    # Deduplicate and keep ascending.
    pts = sorted(set(pts))
    return pts


def _nearly_sorted_array(n: int, rng: random.Random) -> List[int]:
    arr = list(range(n))
    # Perturb a small fraction of elements to simulate "nearly sorted".
    # Keep perturbations small so insertion sort has a fair opportunity.
    swaps = max(1, n // 200)  # ~0.5% of n
    for _ in range(swaps):
        i = rng.randrange(n)
        j = rng.randrange(n)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


@router.post("/benchmark", response_model=BenchmarkResponse)
async def benchmark_endpoint(payload: BenchmarkRequest) -> BenchmarkResponse:
    settings = get_settings()
    if payload.problem_type not in {"sorting", "searching"}:
        # Execution-time benchmarking can be added later for graph/DP; for now, UI falls back to complexity chart.
        return BenchmarkResponse(timings=[])

    rng = random.Random(42)
    sizes = _benchmark_sizes(payload.input_size, settings)

    timings: List[BenchmarkAlgorithmTiming] = []

    if payload.problem_type == "sorting":
        alg_map: Dict[str, Callable[[List[int]], List[int]]] = {
            "Insertion Sort": insertion_sort,
            "Merge Sort": merge_sort,
            "Heap Sort": heap_sort,
            "Quick Sort": quick_sort,
        }

        if payload.algorithms:
            requested = set(payload.algorithms)
            alg_map = {k: v for k, v in alg_map.items() if k in requested}

        for alg_name, fn in alg_map.items():
            # Complexity strings are returned for UI labeling.
            if alg_name == "Insertion Sort":
                time_complexity = "O(n)" if payload.nearly_sorted else "O(n^2)"
                space_complexity = "O(1)"
            elif alg_name == "Quick Sort":
                time_complexity = "O(n log n)"
                space_complexity = "O(log n)"
            elif alg_name in {"Merge Sort", "Heap Sort"}:
                time_complexity = "O(n log n)"
                space_complexity = "O(n)" if alg_name == "Merge Sort" else "O(1)"
            else:
                time_complexity = "O(n log n)"
                space_complexity = "O(1)"

            pts: List[BenchmarkPoint] = []
            for n in sizes:
                total = 0.0
                # Average multiple runs for stability.
                for _ in range(settings.benchmark_sample_counts):
                    if payload.nearly_sorted:
                        arr = _nearly_sorted_array(n, rng)
                    else:
                        arr = [rng.randrange(0, max(10, n * 10)) for _ in range(n)]
                    start = time.perf_counter()
                    _ = fn(arr)
                    end = time.perf_counter()
                    total += (end - start)
                avg_ms = (total / settings.benchmark_sample_counts) * 1000.0
                pts.append(BenchmarkPoint(input_size=n, time_ms=avg_ms))

            timings.append(
                BenchmarkAlgorithmTiming(
                    algorithm=alg_name,
                    time_complexity=time_complexity,
                    timings=pts,
                )
            )

    else:
        # searching
        arr_builder = (
            (lambda n: list(range(n))) if payload.nearly_sorted else (lambda n: [rng.randrange(0, max(10, n * 10)) for _ in range(n)])
        )
        # Ensure binary search receives sorted data.
        def _sorted_if_needed(a: List[int]) -> List[int]:
            return sorted(a) if payload.nearly_sorted is False else a

        alg_map: Dict[str, Callable[[List[int], int], int]] = {
            "Linear Search": linear_search,
            "Binary Search": binary_search,
        }

        if payload.algorithms:
            requested = set(payload.algorithms)
            alg_map = {k: v for k, v in alg_map.items() if k in requested}

        for alg_name, fn in alg_map.items():
            time_complexity = "O(log n)" if alg_name == "Binary Search" else "O(n)"
            pts: List[BenchmarkPoint] = []
            for n in sizes:
                total = 0.0
                for _ in range(settings.benchmark_sample_counts):
                    a = arr_builder(n)
                    if alg_name == "Binary Search":
                        a = _sorted_if_needed(a)
                    # pick target (pick existing element for deterministic hits)
                    target = a[rng.randrange(0, n)] if n > 0 else 0
                    start = time.perf_counter()
                    _ = fn(a, target)
                    end = time.perf_counter()
                    total += (end - start)
                avg_ms = (total / settings.benchmark_sample_counts) * 1000.0
                pts.append(BenchmarkPoint(input_size=n, time_ms=avg_ms))

            timings.append(
                BenchmarkAlgorithmTiming(
                    algorithm=alg_name,
                    time_complexity=time_complexity,
                    timings=pts,
                )
            )

    # Persist benchmark logs (best-effort).
    try:
        mongo = get_mongo_store()
        mongo.save_benchmark_log(
            {
                "request": payload.model_dump(),
                "timings": [t.model_dump() for t in timings],
            }
        )
    except Exception:
        # Benchmark should still return even if Mongo is unavailable.
        pass

    return BenchmarkResponse(timings=timings)

