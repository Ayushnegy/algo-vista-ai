import type { GraphType, MemoryLevel, ProblemType, RecommendationRequest } from '../types'

type Props = {
  value: RecommendationRequest
  loading: boolean
  onChange: (next: RecommendationRequest) => void
  onRecommend: () => void
}

const memoryOptions: MemoryLevel[] = ['low', 'medium', 'high']

export default function InputPanel({ value, loading, onChange, onRecommend }: Props) {
  const set = (patch: Partial<RecommendationRequest>) => onChange({ ...value, ...patch })

  const problemLabel: Record<ProblemType, string> = {
    sorting: 'Sorting',
    searching: 'Searching',
    graph: 'Graph',
    dp: 'Dynamic Programming',
    string: 'String Algorithms',
    greedy: 'Greedy Algorithms',
    backtracking: 'Backtracking',
    divide_and_conquer: 'Divide & Conquer',
  }

  const graphLabel: Record<GraphType, string> = {
    dense: 'Dense',
    sparse: 'Sparse',
  }

  return (
    <div className="card">
      <div className="cardTitle">📋 Configuration Panel</div>

      <div className="row">
        <div className="field floatField">
          <label className="label">🎯 Problem Type</label>
          <select
            className="fancyInput"
            value={value.problem_type}
            onChange={(e) => {
              const nextType = e.target.value as ProblemType
              set({
                problem_type: nextType,
                graph_type: nextType === 'graph' ? (value.graph_type ?? 'dense') : null,
              })
            }}
          >
            {Object.entries(problemLabel).map(([k, v]) => (
              <option key={k} value={k}>
                {v}
              </option>
            ))}
          </select>
        </div>

        <div className="field floatField">
          <label className="label">📊 Input Size (n)</label>
          <input
            className="fancyInput"
            type="number"
            min={1}
            step={1}
            value={value.input_size}
            onChange={(e) => set({ input_size: Math.max(1, Number(e.target.value || 1)) })}
          />
        </div>
      </div>

      <div style={{ height: 12 }} />

      <div className="toggles">
        <label className="toggle switchRow">
          <span>🔄 Nearly Sorted</span>
          <span className="switch">
            <input
              type="checkbox"
              checked={value.nearly_sorted}
              onChange={(e) => set({ nearly_sorted: e.target.checked })}
            />
            <span className="switchSlider" />
          </span>
        </label>

        <label className="toggle switchRow">
          <span>🔀 Recursive Allowed</span>
          <span className="switch">
            <input
              type="checkbox"
              checked={value.recursive_allowed}
              onChange={(e) => set({ recursive_allowed: e.target.checked })}
            />
            <span className="switchSlider" />
          </span>
        </label>

        {value.problem_type === 'graph' && (
          <div className="field floatField" style={{ gridColumn: '1 / -1' }}>
            <label className="label">🕸️ Graph Type</label>
            <select
              className="fancyInput"
              value={(value.graph_type ?? 'dense') as GraphType}
              onChange={(e) => set({ graph_type: e.target.value as GraphType })}
            >
              {(Object.entries(graphLabel) as [GraphType, string][]).map(([k, v]) => (
                <option key={k} value={k}>
                  {v}
                </option>
              ))}
            </select>
          </div>
        )}

        <div className="field" style={{ gridColumn: '1 / -1' }}>
          <div className="label">💾 Memory Constraint</div>
          <div className="seg">
            {memoryOptions.map((m) => (
              <button key={m} type="button" className={value.memory === m ? 'active' : ''} onClick={() => set({ memory: m })}>
                {m[0].toUpperCase() + m.slice(1)}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="actions">
        <button className="primaryBtn rippleBtn" disabled={loading} onClick={onRecommend} type="button">
          {loading ? '✨ Recommending...' : '🚀 Recommend Algorithm'}
        </button>
      </div>

      <div className="smallNote">
        💡 Tip: For "Graph", set dense/sparse. For "DP", memory and recursion settings influence strategy selection.
      </div>
    </div>
  )
}

