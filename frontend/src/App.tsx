import { useMemo, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'

import type { BenchmarkResponse, RecommendationRequest, RecommendationResponse } from './types'
import Header from './components/Header'
import InputPanel from './components/InputPanel'
import OutputPanel from './components/OutputPanel'
import VisualizationSection from './components/visualization/VisualizationSection'
import ComparisonSection from './components/ComparisonSection'
import { benchmark as benchmarkApi, exportPdf, recommend as recommendApi } from './api/client'
import type { ComplexityChartEntry, BenchmarkAlgorithmTiming } from './types'

export default function App() {
  const [req, setReq] = useState<RecommendationRequest>({
    problem_type: 'sorting',
    input_size: 1000,
    nearly_sorted: false,
    memory: 'medium',
    recursive_allowed: true,
    graph_type: 'dense',
  })

  const [loading, setLoading] = useState(false)
  const [benchmarkLoading, setBenchmarkLoading] = useState(false)
  const [exporting, setExporting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showComparison, setShowComparison] = useState(true)

  const [recommendation, setRecommendation] = useState<RecommendationResponse | null>(null)
  const [benchmark, setBenchmark] = useState<BenchmarkResponse | null>(null)

  const complexityEntries: ComplexityChartEntry[] = useMemo(() => recommendation?.complexity_chart ?? [], [recommendation])

  const benchmarkTimings: BenchmarkAlgorithmTiming[] = useMemo(
    () => benchmark?.timings ?? [],
    [benchmark],
  )

  async function onRecommend() {
    setError(null)
    setLoading(true)
    setBenchmarkLoading(true)
    setBenchmark(null)

    try {
      const rec = await recommendApi(req)
      setRecommendation(rec)

      // Benchmark is optional; if backend returns empty, UI will fall back to complexity chart.
      try {
        const bench = await benchmarkApi(req)
        setBenchmark(bench)
      } catch (e: any) {
        setBenchmark({ timings: [] })
      }
    } catch (e: any) {
      setError(e?.message ?? 'Failed to get recommendation.')
    } finally {
      setLoading(false)
      setBenchmarkLoading(false)
    }
  }

  async function onExportPdf() {
    if (!recommendation) return
    setError(null)
    setExporting(true)
    try {
      const blob = await exportPdf(recommendation)
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'AlgoVistaAI_Report.pdf'
      document.body.appendChild(a)
      a.click()
      a.remove()
      URL.revokeObjectURL(url)
    } catch (e: any) {
      setError(e?.message ?? 'Export failed.')
    } finally {
      setExporting(false)
    }
  }

  return (
    <motion.div
      className="container"
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.45, ease: 'easeOut' }}
    >
      <Header />
      
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1, ease: 'easeOut' }}
        style={{ marginTop: 12, marginBottom: 12, textAlign: 'center' }}
      >
        <h2 style={{ margin: '0 0 6px 0', fontSize: '20px', fontWeight: 700, background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          Choose the Right Algorithm, Every Time
        </h2>
        <p style={{ color: '#64748b', fontSize: '14px', margin: 0 }}>
          Let AI analyze your requirements and find the optimal algorithm for your specific use case
        </p>
      </motion.div>

      <div className="grid">
        <motion.div whileHover={{ y: -2 }} transition={{ duration: 0.18 }}>
          <InputPanel value={req} onChange={setReq} loading={loading} onRecommend={onRecommend} />
          <AnimatePresence>
            {error ? (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                className="error"
              >
                {error}
              </motion.div>
            ) : null}
          </AnimatePresence>
        </motion.div>

        <motion.div whileHover={{ y: -2 }} transition={{ duration: 0.18 }}>
          <OutputPanel value={recommendation} onExport={onExportPdf} exporting={exporting} />
        </motion.div>
      </div>

      <AnimatePresence>
        {recommendation ? (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.25 }}
            style={{ marginTop: 16 }}
          >
            <VisualizationSection
              complexity={complexityEntries}
              benchmarkTimings={benchmarkLoading ? [] : benchmarkTimings}
              highlightAlgorithm={recommendation.recommended_algorithm}
            />
            <ComparisonSection
              comparison={recommendation.comparison_algorithms}
              recommendedName={recommendation.recommended_algorithm}
              show={showComparison}
              onToggle={() => setShowComparison((v) => !v)}
            />
          </motion.div>
        ) : null}
      </AnimatePresence>
    </motion.div>
  )
}

