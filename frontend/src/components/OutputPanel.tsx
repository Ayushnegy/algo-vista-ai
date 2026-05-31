import { motion } from 'framer-motion'
import type { RecommendationResponse } from '../types'

type Props = {
  value: RecommendationResponse | null
  onExport?: () => void
  exporting?: boolean
}

export default function OutputPanel({ value, onExport, exporting }: Props) {
  if (!value) {
    return (
      <div className="card">
        <div className="cardTitle">📊 Results</div>
        <div className="hint">✨ Submit inputs on the left to get an AI-powered recommendation with complexity analysis and detailed insights.</div>
      </div>
    )
  }

  return (
    <div className="card">
      <div className="cardTitle">📊 Recommended Solution</div>

      <motion.div
        className="resultAlg"
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.35 }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12 }}>
          <div className="resultAlgName">{value.recommended_algorithm}</div>
          <span className="pill" style={{ background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(34, 197, 94, 0.12))', borderColor: 'rgba(16, 185, 129, 0.35)' }}>
            ✨ Recommended
          </span>
        </div>
        <div className="hint" style={{ marginTop: 0 }}>
          🎯 Decision: <b>{value.decision_layer}</b>
          {value.model_used ? (
            <>
              {' '}
              • 🧠 ML Confidence: <b>{(value.ml_confidence ?? 0).toFixed(2)}</b>
            </>
          ) : null}
        </div>

        <div className="kpiRow">
          <div className="kpi">
            <div className="kpiLabel">⏱ Time Complexity</div>
            <div className="kpiValue">{value.time_complexity}</div>
          </div>
          <div className="kpi">
            <div className="kpiLabel">💾 Space Complexity</div>
            <div className="kpiValue">{value.space_complexity}</div>
          </div>
        </div>

        <div className="hint" style={{ marginTop: 4 }}>
          <b>💡 Why:</b> {value.reason}
        </div>
      </motion.div>

      {value ? (
        <div className="actions" style={{ marginTop: 12 }}>
          <button
            className="primaryBtn"
            disabled={exporting}
            onClick={onExport}
            type="button"
          >
            {exporting ? '⏳ Exporting...' : '📥 Export PDF Report'}
          </button>
        </div>
      ) : null}

      {value.alternatives.length > 0 && (
        <div style={{ marginTop: 14 }}>
          <div className="cardTitle" style={{ marginBottom: 10 }}>
            🔄 Alternative Options
          </div>
          <div className="altList">
            {value.alternatives.map((alt) => (
              <div className="alt" key={alt.algorithm}>
                <div className="altTitle">{alt.algorithm}</div>
                <div className="altMeta">
                  Time: <b>{alt.time_complexity}</b> • Space: <b>{alt.space_complexity}</b>
                </div>
                <div className="altMeta">{alt.short_reason}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

