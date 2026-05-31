import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from 'chart.js'

import type { BenchmarkAlgorithmTiming } from '../../types'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend)

type Props = {
  timings: BenchmarkAlgorithmTiming[]
  highlightAlgorithm?: string
}

const palette = [
  'rgba(59, 130, 246, 0.95)',
  'rgba(56, 189, 248, 0.95)',
  'rgba(99, 102, 241, 0.95)',
  'rgba(14, 165, 233, 0.95)',
  'rgba(37, 99, 235, 0.95)',
]

export default function ExecutionTimeChart({ timings, highlightAlgorithm }: Props) {
  if (!timings || timings.length === 0) {
    return (
      <div>
        <div className="cardTitle" style={{ marginBottom: 8 }}>
          ⏱️ Real-time Performance Benchmark
        </div>
        <div className="hint">Execution-time benchmarking is available for Sorting and Searching inputs.</div>
      </div>
    )
  }

  const xValues = Array.from(
    new Set(timings.flatMap((t) => t.timings.map((p) => p.input_size))).values(),
  ).sort((a, b) => a - b)

  const chartData = {
    labels: xValues.map((x) => String(x)),
    datasets: timings.map((t, idx) => {
      const isHighlight = t.algorithm === highlightAlgorithm
      const color = palette[idx % palette.length]
      const points = xValues.map((x) => {
        const match = t.timings.find((p) => p.input_size === x)
        return match ? match.time_ms : 0
      })

      return {
        label: t.algorithm,
        data: points,
        borderColor: isHighlight ? color : `${color.replace('0.95', '0.45')}`,
        backgroundColor: color,
        pointRadius: isHighlight ? 4 : 2,
        pointHoverRadius: isHighlight ? 6 : 4,
        borderWidth: isHighlight ? 3 : 1.5,
        tension: 0.25,
      }
    }),
  }

  return (
    <div>
      <div className="cardTitle" style={{ marginBottom: 8 }}>
        ⏱️ Execution Time Benchmark (ms)
      </div>
      <div style={{ height: 320 }}>
        <Line
          data={chartData}
          options={{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { position: 'top', align: 'start' as const },
              tooltip: {
                callbacks: {
                  label: (ctx) => `${ctx.dataset.label}: ${(ctx.parsed.y ?? 0).toFixed(2)} ms`,
                },
              },
            },
            scales: {
              y: {
                ticks: { color: '#4b5563' },
                grid: { color: 'rgba(229, 231, 235, 0.7)' },
              },
              x: { ticks: { color: '#4b5563' }, grid: { display: false } },
            },
          }}
        />
      </div>
    </div>
  )
}

