export type ProblemType =
  | 'sorting'
  | 'searching'
  | 'graph'
  | 'dp'
  | 'string'
  | 'greedy'
  | 'backtracking'
  | 'divide_and_conquer'
export type MemoryLevel = 'low' | 'medium' | 'high'
export type GraphType = 'dense' | 'sparse'

export type RecommendationRequest = {
  problem_type: ProblemType
  input_size: number
  nearly_sorted: boolean
  memory: MemoryLevel
  recursive_allowed: boolean
  graph_type?: GraphType | null
}

export type AlternativeAlgorithm = {
  algorithm: string
  time_complexity: string
  space_complexity: string
  short_reason: string
}

export type ComparisonAlgorithm = {
  name: string
  time: string
  space: string
  stability?: 'yes' | 'no' | 'n/a'
  best_case?: string | null
  worst_case?: string | null
  use_case?: string | null
  rank?: 'best' | 'good' | 'not_suitable'
}

export type ComplexityChartEntry = {
  algorithm: string
  time_complexity: string
  growth_score: number
}

export type RecommendationResponse = {
  recommended_algorithm: string
  time_complexity: string
  space_complexity: string
  reason: string
  alternatives: AlternativeAlgorithm[]
  decision_layer: 'rules' | 'ml' | 'ensemble'
  model_used: boolean
  ml_confidence?: number | null
  complexity_chart: ComplexityChartEntry[]
  comparison_algorithms: ComparisonAlgorithm[]
  benchmark_hint?: {
    algorithms?: string[]
    input_sizes?: number[]
    [k: string]: unknown
  }
}

export type BenchmarkPoint = {
  input_size: number
  time_ms: number
}

export type BenchmarkAlgorithmTiming = {
  algorithm: string
  time_complexity: string
  timings: BenchmarkPoint[]
}

export type BenchmarkResponse = {
  timings: BenchmarkAlgorithmTiming[]
}

