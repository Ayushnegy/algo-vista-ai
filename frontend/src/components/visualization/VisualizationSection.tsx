import type { BenchmarkAlgorithmTiming, ComplexityChartEntry } from '../../types'
import ComplexityChart from './ComplexityChart'
import ExecutionTimeChart from './ExecutionTimeChart'

type Props = {
  complexity: ComplexityChartEntry[]
  benchmarkTimings: BenchmarkAlgorithmTiming[]
  highlightAlgorithm?: string
}

export default function VisualizationSection({ complexity, benchmarkTimings, highlightAlgorithm }: Props) {
  return (
    <div className="chartsGrid">
      <div className="card" style={{ padding: 16 }}>
        <ComplexityChart entries={complexity} highlightAlgorithm={highlightAlgorithm} />
      </div>
      <div className="card" style={{ padding: 16 }}>
        <ExecutionTimeChart timings={benchmarkTimings} highlightAlgorithm={highlightAlgorithm} />
      </div>
    </div>
  )
}

