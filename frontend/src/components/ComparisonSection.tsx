import type { ComparisonAlgorithm } from '../types'

type Props = {
  comparison: ComparisonAlgorithm[]
  recommendedName: string
  show: boolean
  onToggle: () => void
}

const rankLabel: Record<NonNullable<ComparisonAlgorithm['rank']>, string> = {
  best: 'Best',
  good: 'Good',
  not_suitable: 'Not suitable',
}

export default function ComparisonSection({ comparison, recommendedName, show, onToggle }: Props) {
  if (!comparison || comparison.length === 0) {
    return null
  }

  return (
    <div style={{ marginTop: 16 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 8, gap: 10 }}>
        <div className="cardTitle" style={{ marginBottom: 0 }}>
          🔀 Side-by-side Comparison
        </div>
        <button
          type="button"
          className="primaryBtn rippleBtn"
          style={{
            padding: '8px 14px',
            fontSize: 12,
            background: show
              ? 'linear-gradient(135deg, var(--primary), var(--accent))'
              : 'rgba(255,255,255,0.9)',
            color: show ? '#fff' : '#64748b',
            border: show ? 'none' : '1px solid #e2e8f0',
            boxShadow: show ? '0 4px 12px rgba(59,130,246,0.2)' : 'none',
          }}
          onClick={onToggle}
        >
          {show ? '👁️ Hide Comparison' : '👁️ Show Comparison'}
        </button>
      </div>

      {show && (
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit,minmax(210px,1fr))',
            gap: 12,
          }}
        >
          {comparison.map((alg) => {
            const isRecommended = alg.name === recommendedName
            const rank = alg.rank ?? (isRecommended ? 'best' : 'good')

            return (
              <div
                key={alg.name}
                className="alt compareCard"
                style={{
                  borderColor: isRecommended ? 'rgba(59,130,246,0.65)' : undefined,
                  boxShadow: isRecommended ? '0 0 0 3px rgba(59,130,246,0.14)' : undefined,
                  background: isRecommended
                    ? 'linear-gradient(135deg, rgba(239,246,255,0.95), rgba(219,234,254,0.85))'
                    : undefined,
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 6 }}>
                  <div className="altTitle">{alg.name}</div>
                  <span
                    className="pill"
                    style={{
                      fontSize: 11,
                      paddingInline: 10,
                      background: rank === 'best' ? 'rgba(59,130,246,0.16)' : 'rgba(229,231,235,0.7)',
                      borderColor: rank === 'best' ? 'rgba(37,99,235,0.45)' : 'rgba(209,213,219,1)',
                    }}
                  >
                    {rankLabel[rank]}
                  </span>
                </div>

                <div className="altMeta" title="Asymptotic worst-case time complexity">
                  Time: <b>{alg.time}</b>
                </div>
                <div className="altMeta" title="Asymptotic extra space complexity">
                  Space: <b>{alg.space}</b>
                </div>
                {alg.best_case ? (
                  <div className="altMeta" title="Best-case complexity">
                    Best-case: <b>{alg.best_case}</b>
                  </div>
                ) : null}
                {alg.worst_case ? (
                  <div className="altMeta" title="Worst-case complexity">
                    Worst-case: <b>{alg.worst_case}</b>
                  </div>
                ) : null}
                <div className="altMeta" title="Is the algorithm stable (preserves relative order)?">
                  Stability:{' '}
                  <b>
                    {alg.stability === 'yes' ? 'Yes' : alg.stability === 'no' ? 'No' : 'N/A'}
                  </b>
                </div>
                {alg.use_case && (
                  <div className="altMeta" style={{ marginTop: 6 }}>
                    {alg.use_case}
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

