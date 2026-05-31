from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple

from app.algorithms import sorting as sorting_impl
from app.schemas import (
    AlternativeAlgorithm,
    ComparisonAlgorithm,
    ComplexityChartEntry,
    MemoryLevel,
    RecommendationRequest,
    RecommendationResponse,
)


def _log2(x: float) -> float:
    return math.log(x, 2)


def growth_score_from_time_complexity(time_complexity: str, n: int) -> float:
    """
    Convert Big-O strings to a comparable monotonic score.
    We use log10(1 + f(n)) to keep values safe across large n.
    """
    n = max(1, n)
    tc = time_complexity.lower().replace(" ", "")

    # Sorting / Searching
    if "logn" in tc and "nlogn" not in tc:
        val = _log2(n)
    elif "nlogn" in tc:
        val = n * _log2(n)
    elif "n^3" in tc or "n**3" in tc:
        val = n ** 3
    elif "n^2" in tc or "n**2" in tc:
        val = n ** 2
    elif "nwd" in tc or "nw" in tc or "n*w" in tc:
        # Generic DP approximation: treat W ~ n/2 => O(nW) ~ O(n^2)
        val = n ** 2
    elif "(n+m)" in tc and "logn" in tc:
        val = n * _log2(n)
    elif "(n+m)" in tc or "n+m" in tc:
        val = n
    elif "2^n" in tc:
        # Avoid huge numbers; log scaling.
        val = n
    else:
        # Default to linear-ish growth if pattern isn't recognized.
        val = n

    return math.log10(1.0 + val)


def _build_entry(algorithm: str, time_complexity: str, space_complexity: str, reason: str, n: int) -> ComplexityChartEntry:
    return ComplexityChartEntry(
        algorithm=algorithm,
        time_complexity=time_complexity,
        growth_score=growth_score_from_time_complexity(time_complexity, n),
    )


def insertion_time_complexity(req: RecommendationRequest) -> str:
    # Insertion sort has best-case O(n) for nearly sorted inputs.
    if req.nearly_sorted:
        return "O(n)"
    return "O(n^2)"


def heap_quick_space_notes(req: RecommendationRequest) -> str:
    # Heap sort is in-place; quicksort recursion uses O(log n) average stack.
    if req.memory == "low":
        return "O(1)"
    return "O(1)"


def _sorting_catalog(req: RecommendationRequest) -> Dict[str, Dict[str, str]]:
    return {
        "Insertion Sort": {
            "time_complexity": insertion_time_complexity(req),
            "space_complexity": "O(1)",
            "reason": "Excellent when the input is already (nearly) sorted due to fast local shifts.",
        },
        "Merge Sort": {
            "time_complexity": "O(n log n)",
            "space_complexity": "O(n)",
            "reason": "Consistently fast for large n with stable O(n log n) behavior.",
        },
        "Heap Sort": {
            "time_complexity": "O(n log n)",
            "space_complexity": "O(1)",
            "reason": "Good worst-case performance with strict memory usage (in-place).",
        },
        "Quick Sort": {
            "time_complexity": "O(n log n)",
            "space_complexity": "O(log n)",
            "reason": "Average-case speed with efficient in-place partitioning (recursion depth ~ log n).",
        },
    }


def _searching_catalog(req: RecommendationRequest) -> Dict[str, Dict[str, str]]:
    return {
        "Binary Search": {
            "time_complexity": "O(log n)",
            "space_complexity": "O(1)",
            "reason": "Leverages sorted order to reduce the search range exponentially.",
        },
        "Linear Search": {
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "reason": "Simple baseline search that works regardless of ordering.",
        },
    }


def _graph_catalog(req: RecommendationRequest) -> Dict[str, Dict[str, str]]:
    return {
        "Dijkstra (Min-Heap)": {
            "time_complexity": "O((n+m) log n)",
            "space_complexity": "O(n)",
            "reason": "Single-source shortest paths on weighted graphs with nonnegative edges (e.g., routing, navigation).",
        },
        "BFS": {
            "time_complexity": "O(n+m)",
            "space_complexity": "O(n)",
            "reason": "Shortest paths in unweighted graphs; explores level by level (e.g., friend-of-friend queries).",
        },
        "Floyd-Warshall": {
            "time_complexity": "O(n^3)",
            "space_complexity": "O(n^2)",
            "reason": "All-pairs shortest paths for smaller dense graphs (e.g., compact road networks, dense interaction graphs).",
        },
    }


def _dp_catalog(req: RecommendationRequest) -> Dict[str, Dict[str, str]]:
    # Problem-oriented DP strategy catalog (kept generic because UI does not pass a DP subtype).
    return {
        "Knapsack 1D Tabulation": {
            "time_complexity": "O(nW)",
            "space_complexity": "O(W)",
            "reason": "Best when memory is constrained and transitions depend only on the previous row (classic knapsack-style DP).",
        },
        "Top-down Memoization": {
            "time_complexity": "O(nW)",
            "space_complexity": "O(nW)",
            "reason": "Useful when many states are unreachable; computes only visited states (e.g., sparse state-space DP).",
        },
        "LCS Tabulation": {
            "time_complexity": "O(n^2)",
            "space_complexity": "O(n^2)",
            "reason": "Standard 2D table DP for sequence alignment/longest common subsequence style problems.",
        },
        "Bitset Subset Sum DP": {
            "time_complexity": "O(nW)",
            "space_complexity": "O(W)",
            "reason": "Bitset transitions are practical for subset-sum/reachability DPs with large integer sets.",
        },
    }


def _string_catalog(req: RecommendationRequest) -> Dict[str, Dict[str, str]]:
    return {
        "KMP": {
            "time_complexity": "O(n + m)",
            "space_complexity": "O(m)",
            "reason": "Linear-time exact substring search via prefix-function preprocessing (e.g., editor search, log scanning).",
        },
        "Rabin-Karp": {
            "time_complexity": "O(n + m)",
            "space_complexity": "O(1)",
            "reason": "Rolling-hash based search suitable for multiple patterns (e.g., plagiarism detection, multi-keyword scan).",
        },
        "Z-Algorithm": {
            "time_complexity": "O(n + m)",
            "space_complexity": "O(n + m)",
            "reason": "Prefix-based pattern matching using the Z-array (e.g., prefix queries, pattern analytics).",
        },
    }


def _greedy_catalog(req: RecommendationRequest) -> Dict[str, Dict[str, str]]:
    return {
        "Activity Selection": {
            "time_complexity": "O(n log n)",
            "space_complexity": "O(1)",
            "reason": "Sort-by-finish-time greedy is optimal for interval scheduling problems.",
        },
        "Huffman Coding": {
            "time_complexity": "O(n log n)",
            "space_complexity": "O(n)",
            "reason": "Creates optimal prefix codes for compression problems using a greedy priority-queue strategy.",
        },
        "Kruskal MST": {
            "time_complexity": "O(m log n)",
            "space_complexity": "O(n)",
            "reason": "Greedy MST algorithm that is effective when edges can be sorted once and processed.",
        },
    }


def _backtracking_catalog(req: RecommendationRequest) -> Dict[str, Dict[str, str]]:
    return {
        "N-Queens (Backtracking)": {
            "time_complexity": "O(N!)",
            "space_complexity": "O(N)",
            "reason": "Systematically explores valid queen placements using constraint pruning.",
        },
        "Sudoku Solver (Backtracking)": {
            "time_complexity": "O(9^(N^2))",
            "space_complexity": "O(N^2)",
            "reason": "Depth-first backtracking with constraints is standard for Sudoku search.",
        },
        "Permutations Generation": {
            "time_complexity": "O(n · n!)",
            "space_complexity": "O(n)",
            "reason": "Elegant choice when all permutations of a small input set are required.",
        },
    }


def _divide_conquer_catalog(req: RecommendationRequest) -> Dict[str, Dict[str, str]]:
    return {
        "Merge Sort": {
            "time_complexity": "O(n log n)",
            "space_complexity": "O(n)",
            "reason": "Canonical divide-and-conquer example that splits, sorts subarrays, and merges them.",
        },
        "Quick Sort": {
            "time_complexity": "O(n log n)",
            "space_complexity": "O(log n)",
            "reason": "Divide-and-conquer via partitioning around a pivot; typically very fast in practice.",
        },
        "Binary Search": {
            "time_complexity": "O(log n)",
            "space_complexity": "O(1)",
            "reason": "Repeatedly halves the search space, embodying divide-and-conquer over sorted arrays.",
        },
    }


def oracle_sorting(req: RecommendationRequest) -> Tuple[str, str]:
    """
    Returns: (recommended_algorithm_name, reason)
    """
    c = _sorting_catalog(req)
    n = req.input_size

    if req.memory == "high" and req.recursive_allowed:
        if req.nearly_sorted:
            if n <= 20000:
                return "Insertion Sort", "Nearly sorted input + enough stack space => insertion is near-linear in practice."
            return "Merge Sort", "Nearly sorted but large n: merge keeps predictable O(n log n) performance with stability."
        return "Merge Sort", "High memory + recursion allowed => merge sort delivers stable O(n log n) for large datasets."

    if req.memory == "low":
        if not req.recursive_allowed:
            return "Heap Sort", "Low memory + recursion not allowed => heap sort avoids extra stack space."
        if req.nearly_sorted and n <= 30000:
            return "Insertion Sort", "Low memory + nearly sorted => insertion sort performs well with O(1) extra space."
        return "Heap Sort", "Low memory => choose an in-place O(1) space algorithm for consistency."

    # medium memory
    if req.nearly_sorted:
        if n <= 50000:
            return "Insertion Sort", "Nearly sorted input => insertion sort tends to be fast while using only O(1) space."
        return "Merge Sort", "Large n with nearly sorted data: merge sort avoids insertion's worst-case O(n^2)."

    if not req.recursive_allowed:
        return "Heap Sort", "Recursion disallowed => avoid recursive quicksort/merge and prefer heap sort."

    # Default: quick sort tends to be fast on average.
    return "Quick Sort", "Balanced tradeoff: quicksort is typically fast (O(n log n) average) while keeping auxiliary space small."


def oracle_searching(req: RecommendationRequest) -> Tuple[str, str]:
    c = _searching_catalog(req)
    if req.nearly_sorted:
        if req.recursive_allowed:
            return "Binary Search", "Array is sorted/nearly sorted => binary search reduces comparisons to O(log n)."
        return "Binary Search", "Sorted input => use iterative binary search to avoid recursion constraints."

    if req.input_size <= 50:
        return "Linear Search", "Small n => simplicity matters; linear search is acceptable and low overhead."

    return "Linear Search", "Unsorted input => binary search cannot be guaranteed; linear scan is robust at O(n)."


def oracle_graph(req: RecommendationRequest) -> Tuple[str, str]:
    c = _graph_catalog(req)
    if req.graph_type == "dense":
        if req.input_size <= 500:
            return "Floyd-Warshall", "Dense graphs with smaller n favor all-pairs Floyd-Warshall (O(n^3))."
        return "Dijkstra (Min-Heap)", "For larger dense graphs, single-source efficiency typically beats O(n^3) when graph is not fully dense in practice."
    # sparse
    if req.memory == "low":
        return "Dijkstra (Min-Heap)", "Sparse + tighter memory => Dijkstra scales well without quadratic memory blow-ups."
    return "Dijkstra (Min-Heap)", "Sparse graphs are best served by Dijkstra with a min-heap."


def oracle_dp(req: RecommendationRequest) -> Tuple[str, str]:
    if req.memory == "low":
        if req.input_size > 20_000:
            return "Bitset Subset Sum DP", "Low memory + large n favors bitset-compressed transitions when the state dimension is value-like."
        return "Knapsack 1D Tabulation", "Low memory favors 1D tabulation to avoid full 2D DP tables."
    if req.memory == "medium":
        if req.recursive_allowed:
            return "Top-down Memoization", "Medium memory + recursion allowed: memoization is effective when the explored state space is sparse."
        return "Knapsack 1D Tabulation", "Recursion disallowed: iterative 1D tabulation gives predictable memory usage."
    # high memory
    if req.recursive_allowed:
        if req.input_size <= 4000:
            return "LCS Tabulation", "High memory with moderate n allows full-table DP for sequence-style problems."
        return "Top-down Memoization", "High memory + recursion allowed supports rich memoization for complex subproblem graphs."
    return "Knapsack 1D Tabulation", "Recursion not allowed => choose iterative DP to avoid call-stack overhead."


def oracle_string(req: RecommendationRequest) -> Tuple[str, str]:
    c = _string_catalog(req)
    if req.input_size <= 1000:
        return "KMP", "For moderate pattern/text sizes, KMP gives linear-time substring search with simple preprocessing."
    return "Rabin-Karp", "For large texts and/or multiple patterns, Rabin-Karp's rolling hash is often more flexible."


def oracle_greedy(req: RecommendationRequest) -> Tuple[str, str]:
    c = _greedy_catalog(req)
    if req.memory == "low":
        return "Activity Selection", "Low memory favors simple interval-scheduling style greedy with O(1) extra space."
    if req.input_size > 10_000:
        return "Kruskal MST", "Large graphs benefit from Kruskal's greedy MST when edges are sortable once."
    return "Huffman Coding", "For encoding/compression-style tasks, Huffman coding is the standard greedy technique."


def oracle_backtracking(req: RecommendationRequest) -> Tuple[str, str]:
    c = _backtracking_catalog(req)
    if not req.recursive_allowed:
        return "Permutations Generation", "When recursion is restricted, keep backtracking to smaller-permutation style problems."
    if req.input_size <= 20:
        return "N-Queens (Backtracking)", "Smaller boards are ideal for constraint-based N-Queens backtracking."
    return "Sudoku Solver (Backtracking)", "For large combinatorial grids, Sudoku-style constraint backtracking is a canonical example."


def oracle_divide_conquer(req: RecommendationRequest) -> Tuple[str, str]:
    c = _divide_conquer_catalog(req)
    if req.input_size <= 64:
        return "Binary Search", "Small inputs on sorted structures are best illustrated with binary search."
    if req.nearly_sorted:
        return "Merge Sort", "Divide-and-conquer merge sort is stable and predictable even when data is nearly sorted."
    return "Quick Sort", "Quick sort showcases divide-and-conquer partitioning and is typically fast for large n."


def _pick_sorting_alternatives(req: RecommendationRequest, recommended: str) -> List[AlternativeAlgorithm]:
    c = _sorting_catalog(req)
    n = req.input_size
    candidates = [a for a in c.keys() if a != recommended]
    # Rank by growth_score (lower is better), with stable preference for merge/insertion.
    candidates.sort(key=lambda name: growth_score_from_time_complexity(c[name]["time_complexity"], n))

    picked = candidates[:3]
    alts: List[AlternativeAlgorithm] = []
    for name in picked:
        alts.append(
            AlternativeAlgorithm(
                algorithm=name,
                time_complexity=c[name]["time_complexity"],
                space_complexity=c[name]["space_complexity"],
                short_reason=c[name]["reason"],
            )
        )
    return alts


def _pick_searching_alternatives(req: RecommendationRequest, recommended: str) -> List[AlternativeAlgorithm]:
    c = _searching_catalog(req)
    n = req.input_size
    candidates = [a for a in c.keys() if a != recommended]
    candidates.sort(key=lambda name: growth_score_from_time_complexity(c[name]["time_complexity"], n))

    alts: List[AlternativeAlgorithm] = []
    for name in candidates[:2]:
        alts.append(
            AlternativeAlgorithm(
                algorithm=name,
                time_complexity=c[name]["time_complexity"],
                space_complexity=c[name]["space_complexity"],
                short_reason=c[name]["reason"],
            )
        )
    return alts


def _pick_graph_alternatives(req: RecommendationRequest, recommended: str) -> List[AlternativeAlgorithm]:
    c = _graph_catalog(req)
    n = req.input_size
    candidates = [a for a in c.keys() if a != recommended]
    candidates.sort(key=lambda name: growth_score_from_time_complexity(c[name]["time_complexity"], n))
    picked = candidates[:2]
    alts: List[AlternativeAlgorithm] = []
    for name in picked:
        alts.append(
            AlternativeAlgorithm(
                algorithm=name,
                time_complexity=c[name]["time_complexity"],
                space_complexity=c[name]["space_complexity"],
                short_reason=c[name]["reason"],
            )
        )
    return alts


def _pick_dp_alternatives(req: RecommendationRequest, recommended: str) -> List[AlternativeAlgorithm]:
    c = _dp_catalog(req)
    n = req.input_size
    candidates = [a for a in c.keys() if a != recommended]
    candidates.sort(key=lambda name: growth_score_from_time_complexity(c[name]["time_complexity"], n))
    picked = candidates[:2]
    alts: List[AlternativeAlgorithm] = []
    for name in picked:
        alts.append(
            AlternativeAlgorithm(
                algorithm=name,
                time_complexity=c[name]["time_complexity"],
                space_complexity=c[name]["space_complexity"],
                short_reason=c[name]["reason"],
            )
        )
    return alts


def _pick_string_alternatives(req: RecommendationRequest, recommended: str) -> List[AlternativeAlgorithm]:
    c = _string_catalog(req)
    n = req.input_size
    candidates = [a for a in c.keys() if a != recommended]
    candidates.sort(key=lambda name: growth_score_from_time_complexity(c[name]["time_complexity"], n))
    picked = candidates[:2]
    alts: List[AlternativeAlgorithm] = []
    for name in picked:
        alts.append(
            AlternativeAlgorithm(
                algorithm=name,
                time_complexity=c[name]["time_complexity"],
                space_complexity=c[name]["space_complexity"],
                short_reason=c[name]["reason"],
            )
        )
    return alts


def _pick_greedy_alternatives(req: RecommendationRequest, recommended: str) -> List[AlternativeAlgorithm]:
    c = _greedy_catalog(req)
    n = req.input_size
    candidates = [a for a in c.keys() if a != recommended]
    candidates.sort(key=lambda name: growth_score_from_time_complexity(c[name]["time_complexity"], n))
    picked = candidates[:2]
    alts: List[AlternativeAlgorithm] = []
    for name in picked:
        alts.append(
            AlternativeAlgorithm(
                algorithm=name,
                time_complexity=c[name]["time_complexity"],
                space_complexity=c[name]["space_complexity"],
                short_reason=c[name]["reason"],
            )
        )
    return alts


def _pick_backtracking_alternatives(req: RecommendationRequest, recommended: str) -> List[AlternativeAlgorithm]:
    c = _backtracking_catalog(req)
    n = req.input_size
    candidates = [a for a in c.keys() if a != recommended]
    candidates.sort(key=lambda name: growth_score_from_time_complexity(c[name]["time_complexity"], n))
    picked = candidates[:2]
    alts: List[AlternativeAlgorithm] = []
    for name in picked:
        alts.append(
            AlternativeAlgorithm(
                algorithm=name,
                time_complexity=c[name]["time_complexity"],
                space_complexity=c[name]["space_complexity"],
                short_reason=c[name]["reason"],
            )
        )
    return alts


def _pick_divide_conquer_alternatives(req: RecommendationRequest, recommended: str) -> List[AlternativeAlgorithm]:
    c = _divide_conquer_catalog(req)
    n = req.input_size
    candidates = [a for a in c.keys() if a != recommended]
    candidates.sort(key=lambda name: growth_score_from_time_complexity(c[name]["time_complexity"], n))
    picked = candidates[:2]
    alts: List[AlternativeAlgorithm] = []
    for name in picked:
        alts.append(
            AlternativeAlgorithm(
                algorithm=name,
                time_complexity=c[name]["time_complexity"],
                space_complexity=c[name]["space_complexity"],
                short_reason=c[name]["reason"],
            )
        )
    return alts


def _catalog_for_request(req: RecommendationRequest) -> Dict[str, Dict[str, str]]:
    if req.problem_type == "sorting":
        return _sorting_catalog(req)
    if req.problem_type == "searching":
        return _searching_catalog(req)
    if req.problem_type == "graph":
        return _graph_catalog(req)
    if req.problem_type == "dp":
        return _dp_catalog(req)
    if req.problem_type == "string":
        return _string_catalog(req)
    if req.problem_type == "greedy":
        return _greedy_catalog(req)
    if req.problem_type == "backtracking":
        return _backtracking_catalog(req)
    if req.problem_type == "divide_and_conquer":
        return _divide_conquer_catalog(req)
    return _sorting_catalog(req)


def _build_comparison_algorithms(
    req: RecommendationRequest,
    catalog: Dict[str, Dict[str, str]],
    recommended: str,
    alternatives: List[AlternativeAlgorithm],
) -> List[ComparisonAlgorithm]:
    """Build enriched comparison entries (2–4 algorithms) with ranking/stability/use-case."""
    comparison: List[ComparisonAlgorithm] = []
    names = [recommended] + [a.algorithm for a in alternatives]

    # Limit to 4 algorithms for readability.
    names = names[:4]

    def profile(algo_name: str) -> Dict[str, Optional[str]]:
        key = algo_name.lower()
        table: Dict[str, Dict[str, Optional[str]]] = {
            "insertion sort": {
                "stability": "yes",
                "best_case": "O(n)",
                "worst_case": "O(n^2)",
                "use_case": "Small or nearly sorted arrays.",
            },
            "merge sort": {
                "stability": "yes",
                "best_case": "O(n log n)",
                "worst_case": "O(n log n)",
                "use_case": "Stable sorting with predictable runtime.",
            },
            "heap sort": {
                "stability": "no",
                "best_case": "O(n log n)",
                "worst_case": "O(n log n)",
                "use_case": "Memory-constrained sorting with strict worst-case guarantees.",
            },
            "quick sort": {
                "stability": "no",
                "best_case": "O(n log n)",
                "worst_case": "O(n^2)",
                "use_case": "Fast practical general-purpose sorting.",
            },
            "binary search": {
                "stability": "n/a",
                "best_case": "O(1)",
                "worst_case": "O(log n)",
                "use_case": "Lookup in sorted arrays.",
            },
            "linear search": {
                "stability": "n/a",
                "best_case": "O(1)",
                "worst_case": "O(n)",
                "use_case": "Unsorted or tiny collections.",
            },
            "dijkstra (min-heap)": {
                "stability": "n/a",
                "best_case": "O((n+m) log n)",
                "worst_case": "O((n+m) log n)",
                "use_case": "Weighted shortest path with nonnegative edges.",
            },
            "bfs": {
                "stability": "n/a",
                "best_case": "O(n+m)",
                "worst_case": "O(n+m)",
                "use_case": "Unweighted shortest path / level traversal.",
            },
            "floyd-warshall": {
                "stability": "n/a",
                "best_case": "O(n^3)",
                "worst_case": "O(n^3)",
                "use_case": "All-pairs shortest paths on small dense graphs.",
            },
            "kmp": {
                "stability": "yes",
                "best_case": "O(n+m)",
                "worst_case": "O(n+m)",
                "use_case": "Deterministic exact pattern matching.",
            },
            "rabin-karp": {
                "stability": "no",
                "best_case": "O(n+m)",
                "worst_case": "O(nm)",
                "use_case": "Multi-pattern matching with rolling hashes.",
            },
            "z-algorithm": {
                "stability": "yes",
                "best_case": "O(n+m)",
                "worst_case": "O(n+m)",
                "use_case": "Prefix-function based pattern analytics.",
            },
            "top-down memoization": {
                "stability": "n/a",
                "best_case": "Depends on visited states",
                "worst_case": "O(nW)",
                "use_case": "Sparse-state dynamic programming.",
            },
            "knapsack 1d tabulation": {
                "stability": "n/a",
                "best_case": "O(nW)",
                "worst_case": "O(nW)",
                "use_case": "Memory-efficient knapsack-style DP.",
            },
            "lcs tabulation": {
                "stability": "n/a",
                "best_case": "O(n^2)",
                "worst_case": "O(n^2)",
                "use_case": "Sequence alignment and LCS-like problems.",
            },
            "bitset subset sum dp": {
                "stability": "n/a",
                "best_case": "O(nW / word_size)",
                "worst_case": "O(nW)",
                "use_case": "Subset-sum reachability with bitset optimization.",
            },
        }
        return table.get(
            key,
            {
                "stability": "n/a",
                "best_case": None,
                "worst_case": None,
                "use_case": None,
            },
        )

    for name in names:
        meta = catalog.get(name)
        if not meta:
            continue

        # Determine baseline suitability based on constraints & problem type.
        rank: str
        algo_lower = name.lower()

        # Default assumption.
        rank = "good"

        # Problem-type aware "not suitable" flags.
        if req.problem_type == "searching":
            if "binary search" in algo_lower and not req.nearly_sorted:
                rank = "not_suitable"
        elif req.problem_type == "sorting":
            n = req.input_size
            if "insertion sort" in algo_lower and (not req.nearly_sorted and n > 50_000):
                rank = "not_suitable"
            if "quick sort" in algo_lower and (not req.recursive_allowed or (req.memory == "low" and n > 50_000)):
                rank = "not_suitable"
        elif req.problem_type == "graph":
            if "floyd-warshall" in algo_lower and req.input_size > 1_000:
                rank = "not_suitable"
        elif req.problem_type == "dp":
            if "top-down memoization" in algo_lower and not req.recursive_allowed:
                rank = "not_suitable"
        elif req.problem_type == "backtracking":
            if ("n-queens" in algo_lower or "sudoku" in algo_lower or "permutations" in algo_lower) and req.input_size > 30:
                rank = "not_suitable"

        # Recommended algorithm is always at least "best".
        if name == recommended:
            rank = "best"

        p = profile(name)
        stability = p["stability"] or "n/a"

        comparison.append(
            ComparisonAlgorithm(
                name=name,
                time=meta["time_complexity"],
                space=meta["space_complexity"],
                stability=stability,
                best_case=p["best_case"],
                worst_case=p["worst_case"],
                use_case=p["use_case"] or meta["reason"],
                rank=rank,
            )
        )

    return comparison


def complexity_chart(req: RecommendationRequest, preferred_algorithms: List[str]) -> List[ComplexityChartEntry]:
    c = _catalog_for_request(req)
    n = req.input_size
    entries: List[ComplexityChartEntry] = []
    for name in preferred_algorithms:
        if name not in c:
            continue
        entries.append(
            _build_entry(
                algorithm=name,
                time_complexity=c[name]["time_complexity"],
                space_complexity=c[name]["space_complexity"],
                reason=c[name]["reason"],
                n=n,
            )
        )
    return entries


def recommend_with_rules(req: RecommendationRequest) -> RecommendationResponse:
    """
    Mandatory rule-based system.
    """
    catalog = _catalog_for_request(req)
    n = req.input_size

    if req.problem_type == "sorting":
        recommended, reason = oracle_sorting(req)
        alternatives = _pick_sorting_alternatives(req, recommended)
    elif req.problem_type == "searching":
        recommended, reason = oracle_searching(req)
        alternatives = _pick_searching_alternatives(req, recommended)
    elif req.problem_type == "graph":
        recommended, reason = oracle_graph(req)
        alternatives = _pick_graph_alternatives(req, recommended)
    elif req.problem_type == "dp":
        recommended, reason = oracle_dp(req)
        alternatives = _pick_dp_alternatives(req, recommended)
    elif req.problem_type == "string":
        recommended, reason = oracle_string(req)
        alternatives = _pick_string_alternatives(req, recommended)
    elif req.problem_type == "greedy":
        recommended, reason = oracle_greedy(req)
        alternatives = _pick_greedy_alternatives(req, recommended)
    elif req.problem_type == "backtracking":
        recommended, reason = oracle_backtracking(req)
        alternatives = _pick_backtracking_alternatives(req, recommended)
    elif req.problem_type == "divide_and_conquer":
        recommended, reason = oracle_divide_conquer(req)
        alternatives = _pick_divide_conquer_alternatives(req, recommended)
    else:
        recommended, reason = oracle_sorting(req)
        alternatives = _pick_sorting_alternatives(req, recommended)

    # Complexity chart includes recommended + alternatives (order by growth score).
    preferred = [recommended] + [a.algorithm for a in alternatives]
    preferred.sort(key=lambda name: growth_score_from_time_complexity(catalog[name]["time_complexity"], n))
    chart = complexity_chart(req, preferred)

    time_complexity = catalog[recommended]["time_complexity"]
    space_complexity = catalog[recommended]["space_complexity"]

    comparison_algorithms = _build_comparison_algorithms(req, catalog, recommended, alternatives)

    return RecommendationResponse(
        recommended_algorithm=recommended,
        time_complexity=time_complexity,
        space_complexity=space_complexity,
        reason=reason,
        alternatives=alternatives,
        decision_layer="rules",
        model_used=False,
        ml_confidence=None,
        complexity_chart=chart,
        comparison_algorithms=comparison_algorithms,
        benchmark_hint={
            "algorithms": preferred[:3],
            "input_sizes": _benchmark_sizes(req),
        },
    )


def recommend_with_overridden_algorithm(
    req: RecommendationRequest,
    recommended_algorithm: str,
    decision_layer: str = "ensemble",
    model_used: bool = True,
    ml_confidence: Optional[float] = None,
) -> RecommendationResponse:
    """
    Rebuild a RecommendationResponse using a forced recommended algorithm.
    This is used when ML suggests an algorithm that differs from the rule oracle.
    """
    catalog = _catalog_for_request(req)
    n = req.input_size

    if recommended_algorithm not in catalog:
        # Fallback to rule oracle if ML suggests something unknown.
        return recommend_with_rules(req)

    # Fetch reason/complexities from catalog. Insertion time depends on req.nearly_sorted.
    time_complexity = catalog[recommended_algorithm]["time_complexity"]
    space_complexity = catalog[recommended_algorithm]["space_complexity"]
    reason = catalog[recommended_algorithm]["reason"]

    if req.problem_type == "sorting":
        alternatives = _pick_sorting_alternatives(req, recommended_algorithm)
    elif req.problem_type == "searching":
        alternatives = _pick_searching_alternatives(req, recommended_algorithm)
    elif req.problem_type == "graph":
        alternatives = _pick_graph_alternatives(req, recommended_algorithm)
    elif req.problem_type == "dp":
        alternatives = _pick_dp_alternatives(req, recommended_algorithm)
    elif req.problem_type == "string":
        alternatives = _pick_string_alternatives(req, recommended_algorithm)
    elif req.problem_type == "greedy":
        alternatives = _pick_greedy_alternatives(req, recommended_algorithm)
    elif req.problem_type == "backtracking":
        alternatives = _pick_backtracking_alternatives(req, recommended_algorithm)
    elif req.problem_type == "divide_and_conquer":
        alternatives = _pick_divide_conquer_alternatives(req, recommended_algorithm)
    else:
        alternatives = _pick_sorting_alternatives(req, recommended_algorithm)

    preferred = [recommended_algorithm] + [a.algorithm for a in alternatives]
    preferred.sort(key=lambda name: growth_score_from_time_complexity(catalog[name]["time_complexity"], n))
    chart = complexity_chart(req, preferred)

    comparison_algorithms = _build_comparison_algorithms(req, catalog, recommended_algorithm, alternatives)

    return RecommendationResponse(
        recommended_algorithm=recommended_algorithm,
        time_complexity=time_complexity,
        space_complexity=space_complexity,
        reason=reason,
        alternatives=alternatives,
        decision_layer=decision_layer if decision_layer in {"rules", "ml", "ensemble"} else "ensemble",
        model_used=model_used,
        ml_confidence=ml_confidence,
        complexity_chart=chart,
        comparison_algorithms=comparison_algorithms,
        benchmark_hint={
            "algorithms": preferred[:3],
            "input_sizes": _benchmark_sizes(req),
        },
    )


def _benchmark_sizes(req: RecommendationRequest) -> List[int]:
    n = req.input_size
    # Keep benchmark sizes small enough to be safe.
    return [max(50, n // 4), max(100, n // 2), max(200, n)]

