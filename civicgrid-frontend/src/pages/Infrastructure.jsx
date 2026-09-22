import { useEffect, useState } from 'react'
import { AlertCircle, Database, Filter } from 'lucide-react'
import { getInfrastructureIndicators } from '../api/infrastructure'

function formatValue(indicator) {
  if (indicator.value === null || indicator.value === undefined) return '—'
  return indicator.unit === 'percent' ? `${indicator.value}%` : indicator.value
}

export default function Infrastructure() {
  const [indicators, setIndicators] = useState([])
  const [allIndicators, setAllIndicators] = useState([])
  const [filters, setFilters] = useState({ category: '', district: '' })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadIndicators() {
      try {
        setLoading(true)
        setError('')

        const params = {}
        if (filters.category) params.category = filters.category
        if (filters.district) params.district = filters.district

        const data = await getInfrastructureIndicators(params)
        const list = Array.isArray(data) ? data : data.results ?? []
        setIndicators(list)

        if (!filters.category && !filters.district) {
          setAllIndicators(list)
        }
      } catch (err) {
        console.error('Unable to load infrastructure indicators:', err)
        setError('Unable to load infrastructure indicators. Please try again.')
      } finally {
        setLoading(false)
      }
    }

    loadIndicators()
  }, [filters.category, filters.district])

  const sourceData = allIndicators.length ? allIndicators : indicators

  const categories = [
    ...new Set(sourceData.map((item) => item.category).filter(Boolean)),
  ]

  const districts = [
    ...new Set(sourceData.map((item) => item.district_name).filter(Boolean)),
  ]

  function updateFilter(name, value) {
    setFilters((current) => ({ ...current, [name]: value }))
  }

  return (
    <section>
      <p className="text-sm font-medium text-blue-700">Infrastructure evidence</p>
      <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">
        Infrastructure Intelligence
      </h1>
      <p className="mt-3 max-w-3xl text-slate-600">
        Review baseline infrastructure indicators that support investment-priority
        decisions.
      </p>

      <div className="mt-7 flex flex-col gap-3 rounded-lg border border-slate-200 bg-white p-4 sm:flex-row">
        <div className="flex items-center gap-2 text-sm font-medium text-slate-600">
          <Filter size={17} /> Filters
        </div>

        <select
          value={filters.district}
          onChange={(event) => updateFilter('district', event.target.value)}
          className="rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500"
        >
          <option value="">All districts</option>
          {districts.map((district) => (
            <option key={district} value={district}>
              {district}
            </option>
          ))}
        </select>

        <select
          value={filters.category}
          onChange={(event) => updateFilter('category', event.target.value)}
          className="rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500"
        >
          <option value="">All categories</option>
          {categories.map((category) => (
            <option key={category} value={category}>
              {category[0].toUpperCase() + category.slice(1)}
            </option>
          ))}
        </select>
      </div>

      {loading && (
        <p className="mt-6 text-slate-600">Loading infrastructure data…</p>
      )}

      {error && (
        <div className="mt-6 flex gap-3 rounded-lg border border-rose-200 bg-rose-50 p-4 text-rose-800">
          <AlertCircle className="shrink-0" size={20} />
          <p>{error}</p>
        </div>
      )}

      {!loading && !error && indicators.length === 0 && (
        <div className="mt-6 rounded-lg border border-slate-200 bg-white p-6 text-slate-600">
          No infrastructure indicators are available for the selected filters.
        </div>
      )}

      {!loading && !error && indicators.length > 0 && (
        <div className="mt-6 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
          {indicators.map((indicator) => (
            <article
              key={indicator.id}
              className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm"
            >
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-500">
                    {indicator.district_name}
                  </p>
                  <h2 className="mt-1 text-lg font-semibold capitalize text-slate-950">
                    {indicator.category} {indicator.indicator}
                  </h2>
                </div>
                <Database className="text-blue-700" size={21} />
              </div>

              <p className="mt-6 text-4xl font-semibold tracking-tight text-slate-950">
                {formatValue(indicator)}
              </p>

              <div className="mt-6 border-t border-slate-100 pt-4 text-sm">
                <p className="text-slate-500">Source</p>
                <p className="mt-1 text-slate-800">
                  {indicator.source || 'Prototype dataset'}
                </p>

                <p className="mt-4 text-slate-500">Data year</p>
                <p className="mt-1 font-medium text-slate-800">
                  {indicator.data_year || 'Not available'}
                </p>
              </div>
            </article>
          ))}
        </div>
      )}

      <div className="mt-6 rounded-lg border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900">
        These are prototype baseline indicators. They are not verified current
        government statistics.
      </div>
    </section>
  )
}