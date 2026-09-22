import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { AlertCircle, ChevronLeft, ChevronRight, Search } from 'lucide-react'
import { getRequests } from '../api/requests'

const PAGE_SIZE = 8

function getPriorityLevel(request) {
  if (request.priority_breakdown?.priority_level) {
    return request.priority_breakdown.priority_level
  }

  if (request.priority_score >= 70) return 'HIGH'
  if (request.priority_score >= 40) return 'MEDIUM'
  return 'LOW'
}

function priorityStyle(priority) {
  const styles = {
    HIGH: 'bg-rose-50 text-rose-700 ring-rose-600/20',
    MEDIUM: 'bg-amber-50 text-amber-700 ring-amber-600/20',
    LOW: 'bg-emerald-50 text-emerald-700 ring-emerald-600/20',
  }

  return styles[priority] ?? styles.LOW
}

export default function Requests() {
  const [requests, setRequests] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [filters, setFilters] = useState({
    category: '',
    location: '',
    status: '',
    search: '',
  })
  const [page, setPage] = useState(1)

  useEffect(() => {
    async function loadRequests() {
      try {
        setLoading(true)
        setError('')

        const params = {}
        if (filters.category) params.category = filters.category
        if (filters.location) params.location = filters.location
        if (filters.status) params.status = filters.status

        const data = await getRequests(params)
        setRequests(Array.isArray(data) ? data : data.results ?? [])
        setPage(1)
      } catch (err) {
        console.error('Unable to load requests:', err)
        setError('Unable to load citizen requests. Please try again.')
      } finally {
        setLoading(false)
      }
    }

    loadRequests()
  }, [filters.category, filters.location, filters.status])

  const categories = useMemo(
    () => [...new Set(requests.map((item) => item.category).filter(Boolean))],
    [requests],
  )

  const locations = useMemo(
    () =>
      [
        ...new Set(
          requests
            .map((item) => item.district_name || item.location)
            .filter(Boolean),
        ),
      ],
    [requests],
  )

  const statuses = useMemo(
    () => [...new Set(requests.map((item) => item.status).filter(Boolean))],
    [requests],
  )

  const visibleRequests = useMemo(() => {
    const searchTerm = filters.search.toLowerCase().trim()

    if (!searchTerm) return requests

    return requests.filter((request) =>
      [request.title, request.location, request.district_name, request.category]
        .filter(Boolean)
        .join(' ')
        .toLowerCase()
        .includes(searchTerm),
    )
  }, [requests, filters.search])

  const totalPages = Math.max(1, Math.ceil(visibleRequests.length / PAGE_SIZE))
  const pageRequests = visibleRequests.slice(
    (page - 1) * PAGE_SIZE,
    page * PAGE_SIZE,
  )

  function updateFilter(name, value) {
    setFilters((current) => ({ ...current, [name]: value }))
    setPage(1)
  }

  return (
    <section>
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div>
          <p className="text-sm font-medium text-blue-700">Citizen demand</p>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">
            Citizen Requests
          </h1>
          <p className="mt-3 text-slate-600">
            Review and prioritize reported infrastructure needs.
          </p>
        </div>
        <p className="text-sm text-slate-500">
          {visibleRequests.length} request{visibleRequests.length === 1 ? '' : 's'} shown
        </p>
      </div>

      <div className="mt-7 grid gap-3 rounded-lg border border-slate-200 bg-white p-4 md:grid-cols-4">
        <label className="relative md:col-span-1">
          <span className="sr-only">Search requests</span>
          <Search
            size={17}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
          />
          <input
            value={filters.search}
            onChange={(event) => updateFilter('search', event.target.value)}
            placeholder="Search requests"
            className="w-full rounded-md border border-slate-300 py-2 pl-9 pr-3 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          />
        </label>

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

        <select
          value={filters.location}
          onChange={(event) => updateFilter('location', event.target.value)}
          className="rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500"
        >
          <option value="">All locations</option>
          {locations.map((location) => (
            <option key={location} value={location}>
              {location}
            </option>
          ))}
        </select>

        <select
          value={filters.status}
          onChange={(event) => updateFilter('status', event.target.value)}
          className="rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500"
        >
          <option value="">All statuses</option>
          {statuses.map((status) => (
            <option key={status} value={status}>
              {status[0].toUpperCase() + status.slice(1)}
            </option>
          ))}
        </select>
      </div>

      {loading && <p className="mt-6 text-slate-600">Loading citizen requests…</p>}

      {error && (
        <div className="mt-6 flex gap-3 rounded-lg border border-rose-200 bg-rose-50 p-4 text-rose-800">
          <AlertCircle className="shrink-0" size={20} />
          <p>{error}</p>
        </div>
      )}

      {!loading && !error && (
        <div className="mt-6 overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm">
          {pageRequests.length === 0 ? (
            <p className="p-6 text-sm text-slate-600">
              No citizen requests match the selected filters.
            </p>
          ) : (
            <>
              <div className="overflow-x-auto">
                <table className="w-full min-w-[900px] text-left text-sm">
                  <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
                    <tr>
                      <th className="px-5 py-3">Priority</th>
                      <th className="px-5 py-3">Request</th>
                      <th className="px-5 py-3">Category</th>
                      <th className="px-5 py-3">Location</th>
                      <th className="px-5 py-3">Language</th>
                      <th className="px-5 py-3">Status</th>
                      <th className="px-5 py-3">Created</th>
                      <th className="px-5 py-3">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {pageRequests.map((request) => {
                      const priority = getPriorityLevel(request)

                      return (
                        <tr key={request.id} className="hover:bg-slate-50">
                          <td className="px-5 py-4">
                            <span
                              className={`rounded-full px-2.5 py-1 text-xs font-semibold ring-1 ${priorityStyle(priority)}`}
                            >
                              {priority}
                            </span>
                          </td>
                          <td className="max-w-sm px-5 py-4 font-medium text-slate-900">
                            {request.title}
                          </td>
                          <td className="px-5 py-4 capitalize text-slate-600">
                            {request.category}
                          </td>
                          <td className="px-5 py-4 text-slate-600">
                            {request.district_name || request.location}
                          </td>
                          <td className="px-5 py-4 text-slate-600">
                            {request.language}
                          </td>
                          <td className="px-5 py-4 capitalize text-slate-600">
                            {request.status}
                          </td>
                          <td className="px-5 py-4 text-slate-600">
                            {request.created_at
                              ? new Date(request.created_at).toLocaleDateString()
                              : '—'}
                          </td>
                          <td className="px-5 py-4">
                            <Link
                              to={`/requests/${request.id}`}
                              className="font-medium text-blue-700 hover:text-blue-900"
                            >
                              View details
                            </Link>
                          </td>
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
              </div>

              <div className="flex items-center justify-between border-t border-slate-200 px-5 py-3">
                <p className="text-sm text-slate-500">
                  Page {page} of {totalPages}
                </p>
                <div className="flex gap-2">
                  <button
                    onClick={() => setPage((current) => Math.max(1, current - 1))}
                    disabled={page === 1}
                    className="inline-flex items-center gap-1 rounded-md border border-slate-300 px-3 py-1.5 text-sm disabled:cursor-not-allowed disabled:opacity-40"
                  >
                    <ChevronLeft size={16} /> Previous
                  </button>
                  <button
                    onClick={() =>
                      setPage((current) => Math.min(totalPages, current + 1))
                    }
                    disabled={page === totalPages}
                    className="inline-flex items-center gap-1 rounded-md border border-slate-300 px-3 py-1.5 text-sm disabled:cursor-not-allowed disabled:opacity-40"
                  >
                    Next <ChevronRight size={16} />
                  </button>
                </div>
              </div>
            </>
          )}
        </div>
      )}
    </section>
  )
}