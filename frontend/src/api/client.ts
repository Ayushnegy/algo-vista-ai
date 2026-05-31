import type {
  BenchmarkResponse,
  RecommendationRequest,
  RecommendationResponse,
} from '../types'

const API_BASE =
  (import.meta as any).env?.VITE_API_URL ||
  'http://localhost:8000'

async function postJson<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(text || `Request failed (${res.status})`)
  }
  return (await res.json()) as T
}

export async function recommend(req: RecommendationRequest): Promise<RecommendationResponse> {
  return postJson<RecommendationResponse>('/recommend', req)
}

export async function benchmark(req: RecommendationRequest): Promise<BenchmarkResponse> {
  return postJson<BenchmarkResponse>('/benchmark', req)
}

export async function exportPdf(recommendation: RecommendationResponse): Promise<Blob> {
  const res = await fetch(`${API_BASE}/export`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ recommendation, format: 'pdf' }),
  })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(text || `Export failed (${res.status})`)
  }
  return await res.blob()
}

