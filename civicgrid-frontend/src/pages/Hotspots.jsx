import { useEffect, useState } from 'react'
import { AlertCircle, MapPinned } from 'lucide-react'
import { getDashboardSummary } from '../api/dashboard'

function demandStyle(level) {
  const styles = {
    HIGH: 'bg-rose-50 text-rose-700 ring-rose-600/20',
    MEDIUM: 'bg-amber-50 text-amber-700 ring-amber-600/20',
    LOW: 'bg-emerald-50 text-emerald-700 ring-emerald-600/20',
  }

  return styles[level] ?? 'bg-slate-100 text-slate-700 ring-slate-200'
}

export default function Hotspots() {
  const [hotspots, setHotspots] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadHotspots() {
      try {
        const data = await getDashboardSummary()

        const list = (data.demand_by_location ?? [])
          .filter(
            (item) => item.location && item.location !== 'unknown',
          )
          .map((item) => ({
            location: item.location,
            request_count: item.count,
            average_priority_score:
              data.average_priority_by_district?.find(
                (district) => district.district === item.location,
              )?.average_priority ?? 0,
            demand_level:
              item.count >= 5
                ? 'HIGH'
                : item.count >= 2
                  ? 'MEDIUM'
                  : 'LOW',
          }))

        setHotspots(list)
      } catch (err) {
        console.error('Unable to load hotspots:', err)
        setError('Unable to load demand hotspots. Please try again.')
      } finally {
        setLoading(false)
      }
    }

    loadHotspots()
  }, [])

  if (loading) {
    return <p className="text-slate-600">Loading demand hotspots…</p>
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
      <p className="text-sm font-medium text-blue-700">
        Concentrated demand
      </p>

      <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">
        Demand Hotspots
      </h1>

      <p className="mt-3 max-w-3xl text-slate-600">
        Identify locations where multiple citizen requests indicate a
        concentrated infrastructure need.
      </p>

      <div className="mt-7 grid gap-6 xl:grid-cols-3">
        <div className="xl:col-span-2">
          {hotspots.length === 0 ? (
            <div className="rounded-lg border border-slate-200 bg-white p-6 text-slate-600">
              No demand hotspots are available yet. Add more citizen
              requests to identify concentrated infrastructure demand.
            </div>
          ) : (
            <div className="grid gap-5 md:grid-cols-2">
              {hotspots.map((hotspot) => (
                <article
                  key={hotspot.location}
                  className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <h2 className="text-lg font-semibold text-slate-950">
                        {hotspot.location}
                      </h2>

                      <p className="mt-1 text-sm text-slate-500">
                        Demand concentration
                      </p>
                    </div>

                    <span
                      className={`rounded-full px-2.5 py-1 text-xs font-semibold ring-1 ${demandStyle(
                        hotspot.demand_level,
                      )}`}
                    >
                      {hotspot.demand_level} DEMAND
                    </span>
                  </div>

                  <dl className="mt-5 grid grid-cols-2 gap-4 border-t border-slate-100 pt-5">
                    <div>
                      <dt className="text-xs uppercase tracking-wide text-slate-500">
                        Requests
                      </dt>

                      <dd className="mt-1 text-xl font-semibold text-slate-900">
                        {hotspot.request_count}
                      </dd>
                    </div>

                    <div>
                      <dt className="text-xs uppercase tracking-wide text-slate-500">
                        Avg. Priority
                      </dt>

                      <dd className="mt-1 text-xl font-semibold text-slate-900">
                        {hotspot.average_priority_score}
                      </dd>
                    </div>
                  </dl>
                </article>
              ))}
            </div>
          )}
        </div>

        <aside className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <MapPinned className="text-blue-700" size={24} />

          <h2 className="mt-4 font-semibold text-slate-950">
            District overview
          </h2>

          <p className="mt-2 text-sm leading-6 text-slate-600">
            Geospatial visualization is coming soon. This view does not
            infer or display geographic coordinates without backend-provided
            map data.
          </p>
        </aside>
      </div>
    </section>
  )
}