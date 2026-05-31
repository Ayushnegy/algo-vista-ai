from typing import Any, Dict, List, Literal, Optional

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, model_validator


MemoryLevel = Literal["low", "medium", "high"]
ProblemType = Literal[
    "sorting",
    "searching",
    "graph",
    "dp",
    "string",
    "greedy",
    "backtracking",
    "divide_and_conquer",
]
GraphType = Literal["dense", "sparse"]


class RecommendationRequest(BaseModel):
    problem_type: ProblemType
    input_size: int = Field(..., gt=0, le=500000)

    # For arrays: whether the array is already sorted or nearly sorted.
    # For sorting: nearly sorted input.
    nearly_sorted: bool = Field(
        default=False,
        validation_alias=AliasChoices("nearly_sorted", "sorted"),
    )

    memory: MemoryLevel
    recursive_allowed: bool = Field(default=True)

    # Only relevant for graph problems.
    graph_type: Optional[GraphType] = None

    @model_validator(mode="after")
    def validate_graph_type(self) -> "RecommendationRequest":
        if self.problem_type == "graph":
            if not self.graph_type:
                raise ValueError("graph_type is required when problem_type is 'graph'")
        else:
            # Ignore graph_type for non-graph problems.
            self.graph_type = None
        return self


class AlternativeAlgorithm(BaseModel):
    algorithm: str
    time_complexity: str
    space_complexity: str
    short_reason: str


class ComparisonAlgorithm(BaseModel):
    name: str
    time: str
    space: str
    stability: Optional[Literal["yes", "no", "n/a"]] = None
    best_case: Optional[str] = None
    worst_case: Optional[str] = None
    use_case: Optional[str] = None
    rank: Optional[Literal["best", "good", "not_suitable"]] = None


class ComplexityChartEntry(BaseModel):
    algorithm: str
    time_complexity: str
    growth_score: float


class RecommendationResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    recommended_algorithm: str
    time_complexity: str
    space_complexity: str
    reason: str

    alternatives: List[AlternativeAlgorithm] = Field(default_factory=list)

    # Decision/ML metadata (helps explain why you got a recommendation).
    decision_layer: Literal["rules", "ml", "ensemble"] = "rules"
    model_used: bool = False
    ml_confidence: Optional[float] = None

    complexity_chart: List[ComplexityChartEntry] = Field(default_factory=list)

    # Helpful for client-side charting; not exhaustive, but avoids extra parsing.
    benchmark_hint: Dict[str, Any] = Field(default_factory=dict)

    # Side-by-side comparison metadata.
    comparison_algorithms: List[ComparisonAlgorithm] = Field(default_factory=list)


class BenchmarkRequest(BaseModel):
    problem_type: ProblemType
    input_size: int = Field(..., gt=0, le=500000)

    nearly_sorted: bool = Field(
        default=False,
        validation_alias=AliasChoices("nearly_sorted", "sorted"),
    )
    memory: MemoryLevel
    recursive_allowed: bool = True
    graph_type: Optional[GraphType] = None

    # Optional filter; if omitted, backend picks relevant algorithms.
    algorithms: Optional[List[str]] = None

    @model_validator(mode="after")
    def validate_graph_type(self) -> "BenchmarkRequest":
        if self.problem_type == "graph":
            if not self.graph_type:
                raise ValueError("graph_type is required when problem_type is 'graph'")
        else:
            self.graph_type = None
        return self


class BenchmarkPoint(BaseModel):
    input_size: int
    time_ms: float


class BenchmarkAlgorithmTiming(BaseModel):
    algorithm: str
    time_complexity: str
    timings: List[BenchmarkPoint]


class BenchmarkResponse(BaseModel):
    timings: List[BenchmarkAlgorithmTiming] = Field(default_factory=list)


class ExportReportRequest(BaseModel):
    recommendation: RecommendationResponse
    # Minimal options: keep it simple.
    format: Literal["pdf"] = "pdf"

