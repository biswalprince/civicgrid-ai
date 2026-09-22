import { useEffect, useState } from 'react'
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { AlertCircle, Building2, FileText, MapPinned, TrendingUp } from 'lucide-react'
import { getRequests } from '../api/requests'
import { getHotspots } from '../api/hotspots'
import { getInfrastructureIndicators } from '../api/infrastructure'

function asList(data) {
  if (Array.isArray(data)) return data
  if (Array.isArray(data?.results)) return data.results
  return data ? [data] : []
}

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

function KpiCard({ label, value, detail, icon: Icon }) {
  return (
    <article className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-600">{label}</p>
          <p className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">
            {value}
          </p>
        </div>
        <div className="rounded-md bg-blue-50 p-2.5 text-blue-700">
          <Icon size={20} />
        </div>
      </div>
      <p className="mt-4 text-xs text-slate-500">{detail}</p>
    </article>
  )
}

export default function Dashboard() {
  const [data, setData] = useState({
    requests: [],
    hotspots: [],
    indicators: [],
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadDashboard() {
      try {
        setLoading(true)
        setError('')

        const [requestsData, hotspotsData, indicatorsData] = await Promise.all([
          getRequests(),
          getHotspots(),
          getInfrastructureIndicators(),
        ])

        setData({
          requests: asList(requestsData),
          hotspots: asList(hotspotsData),
          indicators: asList(indicatorsData),
        })
      } catch (err) {
        console.error('Unable to load dashboard data:', err)
        setError('Unable to load dashboard data. Please try again.')
      } finally {
        setLoading(false)
      }
    }

    loadDashboard()
  }, [])

  if (loading) {
    return <p className="text-slate-600">Loading infrastructure intelligence…</p>
  }

  if (error) {
    return (
      <div className="flex gap-3 rounded-lg border border-rose-200 bg-rose-50 p-4 text-rose-800">
        <AlertCircle className="mt-0.5 shrink-0" size={20} />
        <p>{error}</p>
      </div>
    )
  }

  const priorityCounts = ['HIGH', 'MEDIUM', 'LOW'].map((level) => ({
    priority: level,
    requests: data.requests.filter(
      (request) => getPriorityLevel(request) === level,
    ).length,
  }))

  const locationCounts = Object.entries(
    data.requests.reduce((counts, request) => {
      const location = request.district_name || request.location || 'Unspecified'
      counts[location] = (counts[location] || 0) + 1
      return counts
    }, {}),
  )
    .map(([location, requests]) => ({ location, requests }))
    .sort((a, b) => b.requests - a.requests)
    .slice(0, 6)

  const highPriorityRequests = data.requests
    .filter((request) => getPriorityLevel(request) === 'HIGH')
    .sort((a, b) => b.priority_score - a.priority_score)
    .slice(0, 5)

  return (
    <section>
      <div>
        <p className="text-sm font-medium text-blue-700">Decision overview</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">
          Infrastructure priorities
        </h1>
        <p className="mt-3 max-w-3xl text-slate-600">
          Review citizen demand, infrastructure evidence, and AI-supported
          recommendations to identify where intervention is needed first.
        </p>
      </div>

      <div className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <KpiCard
          label="Total Requests"
          value={data.requests.length}
          detail="Citizen infrastructure requests received"
          icon={FileText}
        />
        <KpiCard
          label="High Priority"
          value={priorityCounts[0].requests}
          detail="Requests requiring urgent attention"
          icon={TrendingUp}
        />
        <KpiCard
          label="Demand Hotspots"
          value={data.hotspots.length}
          detail="Locations with concentrated demand"
          icon={MapPinned}
        />
        <KpiCard
          label="Infrastructure Indicators"
          value={data.indicators.length}
          detail="Prototype baseline data points"
          icon={Building2}
        />
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-2">
        <article className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <h2 className="font-semibold text-slate-950">Priority distribution</h2>
          <p className="mt-1 text-sm text-slate-500">
            How many requests need urgent intervention?
          </p>

          <div className="mt-6 h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={priorityCounts}>
                <CartesianGrid vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="priority" tickLine={false} axisLine={false} />
                <YAxis allowDecimals={false} tickLine={false} axisLine={false} />
                <Tooltip />
                <Bar dataKey="requests" fill="#2563eb" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </article>

        <article className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <h2 className="font-semibold text-slate-950">Demand by location</h2>
          <p className="mt-1 text-sm text-slate-500">
            Where are citizen needs most concentrated?
          </p>

          <div className="mt-6 h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={locationCounts}>
                <CartesianGrid vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="location" tickLine={false} axisLine={false} />
                <YAxis allowDecimals={false} tickLine={false} axisLine={false} />
                <Tooltip />
                <Bar dataKey="requests" fill="#0f766e" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </article>
      </div>

      <article className="mt-6 rounded-lg border border-slate-200 bg-white shadow-sm">
        <div className="border-b border-slate-200 px-5 py-4">
          <h2 className="font-semibold text-slate-950">Recent high-priority requests</h2>
          <p className="mt-1 text-sm text-slate-500">
            Requests policymakers should review first.
          </p>
        </div>

        {highPriorityRequests.length === 0 ? (
          <p className="p-5 text-sm text-slate-600">
            No high-priority requests are currently available.
          </p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full min-w-[700px] text-left text-sm">
              <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
                <tr>
                  <th className="px-5 py-3">Request</th>
                  <th className="px-5 py-3">Location</th>
                  <th className="px-5 py-3">Category</th>
                  <th className="px-5 py-3">Priority score</th>
                  <th className="px-5 py-3">Priority</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {highPriorityRequests.map((request) => {
                  const priority = getPriorityLevel(request)

                  return (
                    <tr key={request.id}>
                      <td className="max-w-md px-5 py-4 font-medium text-slate-900">
                        {request.title}
                      </td>
                      <td className="px-5 py-4 text-slate-600">
                        {request.district_name || request.location}
                      </td>
                      <td className="px-5 py-4 capitalize text-slate-600">
                        {request.category}
                      </td>
                      <td className="px-5 py-4 font-medium text-slate-900">
                        {request.priority_score}
                      </td>
                      <td className="px-5 py-4">
                        <span
                          className={`rounded-full px-2.5 py-1 text-xs font-semibold ring-1 ${priorityStyle(priority)}`}
                        >
                          {priority}
                        </span>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        )}
      </article>
    </section>
  )
}