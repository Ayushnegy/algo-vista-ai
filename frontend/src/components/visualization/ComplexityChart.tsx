import { Bar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from 'chart.js'

import type { ComplexityChartEntry } from '../../types'

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend)

type Props = {
  entries: ComplexityChartEntry[]
  highlightAlgorithm?: string
}

export default function ComplexityChart({ entries, highlightAlgorithm }: Props) {
  const labels = entries.map((e) => e.algorithm)
  const data = entries.map((e) => e.growth_score)

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Growth Score (log-scaled)',
        data,
        backgroundColor: labels.map((name) =>
          name === highlightAlgorithm ? 'rgba(59, 130, 246, 0.55)' : 'rgba(59, 130, 246, 0.18)',
        ),
        borderColor: labels.map((name) =>
          name === highlightAlgorithm ? 'rgba(37, 99, 235, 0.9)' : 'rgba(148, 163, 184, 0.8)',
        ),
        borderWidth: labels.map((name) => (name === highlightAlgorithm ? 2 : 1)),
        borderRadius: 10,
      },
    ],
  }

  return (
    <div>
      <div className="cardTitle" style={{ marginBottom: 8 }}>
        📈 Time Complexity Growth
      </div>
      <div style={{ height: 320 }}>
        <Bar
          data={chartData}
          options={{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { display: false },
              tooltip: {
                callbacks: {
                  label: (ctx) => {
                    const idx = ctx.dataIndex
                    const entry = entries[idx]
                    return `${entry.time_complexity} • score=${entry.growth_score.toFixed(3)}`
                  },
                },
              },
            },
            scales: {
              y: {
                beginAtZero: true,
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

