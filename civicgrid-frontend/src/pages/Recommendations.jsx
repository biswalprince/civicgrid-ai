import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { AlertCircle, Bot, LoaderCircle, Sparkles } from 'lucide-react'
import { getRequests } from '../api/requests'
import { generateRecommendation } from '../api/recommendations'

function getPriorityLevel(request) {
  return (
    request.priority_breakdown?.priority_level ??
    (request.priority_score >= 70
      ? 'HIGH'
      : request.priority_score >= 40
        ? 'MEDIUM'
        : 'LOW')
  )
}

function priorityStyle(priority) {
  const styles = {
    HIGH: 'bg-rose-50 text-rose-700',
    MEDIUM: 'bg-amber-50 text-amber-700',
    LOW: 'bg-emerald-50 text-emerald-700',
  }

  return styles[priority] ?? 'bg-slate-100 text-slate-700'
}

export default function Recommendations() {
  const [requests, setRequests] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [recommendations, setRecommendations] = useState({})
  const [generatingId, setGeneratingId] = useState(null)
  const [recommendationError, setRecommendationError] = useState('')

  useEffect(() => {
    async function loadRequests() {
      try {
        const data = await getRequests()
        setRequests(Array.isArray(data) ? data : data.results ?? [])
      } catch (err) {
        console.error('Unable to load recommendation requests:', err)
        setError('Unable to load requests for AI recommendations.')
      } finally {
        setLoading(false)
      }
    }

    loadRequests()
  }, [])

  async function handleGenerate(requestId) {
    try {
      setGeneratingId(requestId)
      setRecommendationError('')

      const data = await generateRecommendation(requestId)

      setRecommendations((current) => ({
        ...current,
        [requestId]: data.recommendation,
      }))
    } catch (err) {
      console.error('Unable to generate recommendation:', err)
      setRecommendationError(
        'Unable to generate the AI recommendation. Please try again.',
      )
    } finally {
      setGeneratingId(null)
    }
  }

  if (loading) {
    return <p className="text-slate-600">Loading AI recommendation candidates…</p>
  }

  if (error) {
    return (
      <div className="flex gap-3 rounded-lg border border-rose-200 bg-rose-50 p-4 text-rose-800">
        <AlertCircle className="shrink-0" size={20} />
        <p>{error}</p>
      </div>
    )
  }

  return (
    <section>
      <p className="text-sm font-medium text-blue-700">Decision support</p>
      <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">
        AI Recommendations
      </h1>
      <p className="mt-3 max-w-3xl text-slate-600">
        Generate evidence-based infrastructure project recommendations for citizen
        requests requiring policy review.
      </p>

      {recommendationError && (
        <div className="mt-6 flex gap-3 rounded-lg border border-rose-200 bg-rose-50 p-4 text-rose-800">
          <AlertCircle className="shrink-0" size={20} />
          <p>{recommendationError}</p>
        </div>
      )}

      {requests.length === 0 ? (
        <div className="mt-7 rounded-lg border border-slate-200 bg-white p-6 text-slate-600">
          No citizen requests are available for AI recommendations.
        </div>
      ) : (
        <div className="mt-7 space-y-5">
          {requests
            .slice()
            .sort((a, b) => b.priority_score - a.priority_score)
            .map((request) => {
              const priority = getPriorityLevel(request)
              const recommendation = recommendations[request.id]
              const isGenerating = generatingId === request.id

              return (
                <article
                  key={request.id}
                  className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm"
                >
                  <div className="flex flex-col justify-between gap-5 lg:flex-row">
                    <div className="max-w-2xl">
                      <div className="flex flex-wrap items-center gap-3">
                        <span
                          className={`rounded-full px-2.5 py-1 text-xs font-semibold ${priorityStyle(priority)}`}
                        >
                          {priority} PRIORITY
                        </span>
                        <span className="text-sm text-slate-500">
                          {request.district_name || request.location}
                        </span>
                      </div>

                      <h2 className="mt-4 text-lg font-semibold text-slate-950">
                        {request.title}
                      </h2>

                      <p className="mt-2 text-sm text-slate-600">
                        Priority score: {request.priority_score} · Category:{' '}
                        <span className="capitalize">{request.category}</span>
                      </p>
                    </div>

                    <div className="flex shrink-0 items-start gap-3">
                      <Link
                        to={`/requests/${request.id}`}
                        className="rounded-md border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
                      >
                        View Request
                      </Link>

                      <button
                        onClick={() => handleGenerate(request.id)}
                        disabled={isGenerating}
                        className="inline-flex items-center gap-2 rounded-md bg-blue-700 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-800 disabled:cursor-not-allowed disabled:opacity-60"
                      >
                        {isGenerating ? (
                          <LoaderCircle size={16} className="animate-spin" />
                        ) : (
                          <Sparkles size={16} />
                        )}
                        {isGenerating ? 'Generating…' : 'Generate'}
                      </button>
                    </div>
                  </div>

                  {recommendation && (
                    <div className="mt-6 rounded-lg border border-blue-100 bg-blue-50 p-5">
                      <div className="flex items-center gap-2 text-blue-800">
                        <Bot size={19} />
                        <p className="text-sm font-semibold">AI Project Recommendation</p>
                      </div>

                      <h3 className="mt-4 text-lg font-semibold text-slate-950">
                        {recommendation.recommended_project}
                      </h3>

                      <div className="mt-4 grid gap-4 md:grid-cols-3">
                        <div>
                          <p className="text-xs font-medium uppercase text-slate-500">
                            Target area
                          </p>
                          <p className="mt-1 text-sm text-slate-800">
                            {recommendation.target_area}
                          </p>
                        </div>
                        <div>
                          <p className="text-xs font-medium uppercase text-slate-500">
                            Expected impact
                          </p>
                          <p className="mt-1 text-sm font-semibold text-slate-800">
                            {recommendation.expected_impact}
                          </p>
                        </div>
                        <div>
                          <p className="text-xs font-medium uppercase text-slate-500">
                            Implementation priority
                          </p>
                          <p className="mt-1 text-sm font-semibold text-slate-800">
                            {recommendation.implementation_priority}
                          </p>
                        </div>
                      </div>

                      <p className="mt-4 border-t border-blue-100 pt-4 text-sm leading-6 text-slate-700">
                        {recommendation.reason}
                      </p>
                    </div>
                  )}
                </article>
              )
            })}
        </div>
      )}
    </section>
  )
}