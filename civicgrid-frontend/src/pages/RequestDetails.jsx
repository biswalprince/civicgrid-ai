import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { AlertCircle, ArrowLeft, Bot, LoaderCircle } from 'lucide-react'
import { getRequests } from '../api/requests'
import { generateRecommendation } from '../api/recommendations'

export default function RequestDetails() {
  const { id } = useParams()
  const [request, setRequest] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [recommendation, setRecommendation] = useState(null)
  const [generating, setGenerating] = useState(false)
  const [recommendationError, setRecommendationError] = useState('')

  useEffect(() => {
    async function loadRequest() {
      try {
        const data = await getRequests()
        const requests = Array.isArray(data) ? data : data.results ?? []
        const selectedRequest = requests.find(
          (item) => String(item.id) === String(id),
        )

        if (!selectedRequest) {
          setError('The requested citizen report could not be found.')
          return
        }

        setRequest(selectedRequest)
      } catch {
        setError('Unable to load request details.')
      } finally {
        setLoading(false)
      }
    }

    loadRequest()
  }, [id])

  async function handleGenerateRecommendation() {
    try {
      setGenerating(true)
      setRecommendationError('')
      const data = await generateRecommendation(id)
      setRecommendation(data.recommendation)
    } catch {
      setRecommendationError(
        'Unable to generate an AI recommendation. Please try again.',
      )
    } finally {
      setGenerating(false)
    }
  }

  if (loading) return <p className="text-slate-600">Loading request details…</p>

  if (error) {
    return (
      <div className="rounded-lg border border-rose-200 bg-rose-50 p-4 text-rose-800">
        {error}
      </div>
    )
  }

  const breakdown = request.priority_breakdown ?? {}

  return (
    <section>
      <Link
        to="/requests"
        className="inline-flex items-center gap-2 text-sm font-medium text-blue-700 hover:text-blue-900"
      >
        <ArrowLeft size={16} /> Back to requests
      </Link>

      <div className="mt-6 grid gap-6 xl:grid-cols-3">
        <div className="space-y-6 xl:col-span-2">
          <article className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-sm font-medium text-blue-700">Citizen request</p>
            <h1 className="mt-2 text-2xl font-semibold text-slate-950">
              {request.title}
            </h1>
            <p className="mt-4 leading-7 text-slate-600">{request.description}</p>

            <dl className="mt-6 grid gap-4 border-t border-slate-200 pt-5 sm:grid-cols-2">
              <div><dt className="text-xs uppercase text-slate-500">Category</dt><dd className="mt-1 capitalize">{request.category}</dd></div>
              <div><dt className="text-xs uppercase text-slate-500">Location</dt><dd className="mt-1">{request.district_name || request.location}</dd></div>
              <div><dt className="text-xs uppercase text-slate-500">Language</dt><dd className="mt-1">{request.language}</dd></div>
              <div><dt className="text-xs uppercase text-slate-500">Status</dt><dd className="mt-1 capitalize">{request.status}</dd></div>
            </dl>
          </article>

          <article className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-950">Priority Analysis</h2>
            <p className="mt-1 text-sm text-slate-500">
              Evidence used to determine intervention urgency.
            </p>

            <div className="mt-6 grid gap-4 sm:grid-cols-2">
              {[
                ['Severity', `${request.severity}/10`],
                ['Population Impact Indicator', `${request.affected_population}/10`],
                ['Infrastructure Gap', `${request.infrastructure_gap}/10`],
                ['Vulnerability', `${request.vulnerability}/10`],
              ].map(([label, value]) => (
                <div key={label} className="rounded-md bg-slate-50 p-4">
                  <p className="text-sm text-slate-500">{label}</p>
                  <p className="mt-1 text-xl font-semibold text-slate-900">{value}</p>
                </div>
              ))}
            </div>

            <div className="mt-6 border-t border-slate-200 pt-5">
              <div className="flex justify-between py-2"><span>Base score</span><strong>{breakdown.base_score ?? request.priority_score}</strong></div>
              <div className="flex justify-between py-2"><span>Context multiplier</span><strong>{breakdown.context_multiplier ?? '—'}</strong></div>
              <div className="flex justify-between border-t border-slate-200 py-3 text-lg"><span>Final score</span><strong>{breakdown.final_score ?? request.priority_score}</strong></div>
            </div>
          </article>
        </div>

        <aside className="h-fit rounded-lg border border-blue-200 bg-blue-50 p-6">
          <div className="flex items-center gap-2 text-blue-800">
            <Bot size={20} />
            <h2 className="font-semibold">AI Project Recommendation</h2>
          </div>

          {!recommendation ? (
            <>
              <p className="mt-4 text-sm leading-6 text-slate-700">
                Generate an evidence-based project recommendation for this request.
              </p>
              <button
                onClick={handleGenerateRecommendation}
                disabled={generating}
                className="mt-5 inline-flex w-full items-center justify-center gap-2 rounded-md bg-blue-700 px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-800 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {generating && <LoaderCircle size={17} className="animate-spin" />}
                {generating
                  ? 'Analyzing infrastructure context…'
                  : 'Generate Recommendation'}
              </button>
            </>
          ) : (
            <div className="mt-5 space-y-4">
              <div>
                <p className="text-xs font-medium uppercase text-blue-700">Recommended project</p>
                <p className="mt-1 font-semibold text-slate-950">{recommendation.recommended_project}</p>
              </div>
              <div><p className="text-xs font-medium uppercase text-blue-700">Target area</p><p className="mt-1">{recommendation.target_area}</p></div>
              <div><p className="text-xs font-medium uppercase text-blue-700">Why this project?</p><p className="mt-1 text-sm leading-6">{recommendation.reason}</p></div>
              <div className="grid grid-cols-2 gap-3">
                <div><p className="text-xs text-slate-500">Expected impact</p><p className="mt-1 font-semibold">{recommendation.expected_impact}</p></div>
                <div><p className="text-xs text-slate-500">Implementation</p><p className="mt-1 font-semibold">{recommendation.implementation_priority}</p></div>
              </div>
            </div>
          )}

          {recommendationError && (
            <div className="mt-4 flex gap-2 text-sm text-rose-700">
              <AlertCircle size={18} /> {recommendationError}
            </div>
          )}
        </aside>
      </div>
    </section>
  )
}