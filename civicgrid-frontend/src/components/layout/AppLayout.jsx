import { useEffect, useState } from 'react'
import { NavLink, Outlet } from 'react-router-dom'
import {
  Bot,
  Building2,
  FileText,
  LayoutDashboard,
  MapPinned,
} from 'lucide-react'
import { checkHealth } from '../../api/health'

const navigation = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/requests', label: 'Citizen Requests', icon: FileText },
  { to: '/hotspots', label: 'Demand Hotspots', icon: MapPinned },
  { to: '/infrastructure', label: 'Infrastructure', icon: Building2 },
  { to: '/recommendations', label: 'AI Recommendations', icon: Bot },
]

export default function AppLayout() {
  const [backendStatus, setBackendStatus] = useState('checking')

  useEffect(() => {
    async function getHealth() {
      try {
        const data = await checkHealth()
        setBackendStatus(data.status === 'ok' ? 'online' : 'offline')
      } catch {
        setBackendStatus('offline')
      }
    }

    getHealth()
  }, [])

  const isOnline = backendStatus === 'online'

  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <div className="flex min-h-screen">
        <aside className="hidden w-64 flex-col border-r border-slate-200 bg-slate-950 p-5 text-slate-200 md:flex">
          <div className="mb-10 flex items-center gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-lg bg-blue-600">
              <Building2 size={22} />
            </div>
            <div>
              <p className="font-semibold text-white">CivicGrid AI</p>
              <p className="text-xs text-slate-400">Infrastructure Intelligence</p>
            </div>
          </div>

          <nav className="space-y-1">
            {navigation.map(({ to, label, icon: Icon }) => (
              <NavLink
                key={to}
                to={to}
                end={to === '/'}
                className={({ isActive }) =>
                  `flex items-center gap-3 rounded-md px-3 py-2.5 text-sm font-medium transition ${
                    isActive
                      ? 'bg-blue-600 text-white'
                      : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                  }`
                }
              >
                <Icon size={18} />
                {label}
              </NavLink>
            ))}
          </nav>

          <div className="mt-auto border-t border-slate-800 pt-5">
            <p className="text-xs uppercase tracking-wide text-slate-500">
              Backend status
            </p>
            <div className="mt-2 flex items-center gap-2 text-sm">
              <span
                className={`h-2.5 w-2.5 rounded-full ${
                  isOnline
                    ? 'bg-emerald-400'
                    : backendStatus === 'checking'
                      ? 'bg-amber-400'
                      : 'bg-rose-400'
                }`}
              />
              <span>
                {isOnline
                  ? 'Backend Online'
                  : backendStatus === 'checking'
                    ? 'Checking backend…'
                    : 'Backend Offline'}
              </span>
            </div>
          </div>
        </aside>

        <main className="min-w-0 flex-1">
          <header className="flex h-16 items-center justify-between border-b border-slate-200 bg-white px-6">
            <div>
              <p className="text-sm font-semibold text-slate-900">CivicGrid AI</p>
              <p className="text-xs text-slate-500">
                Public infrastructure decision support
              </p>
            </div>

            <div className="flex items-center gap-2 text-sm text-slate-600">
              <span
                className={`h-2.5 w-2.5 rounded-full ${
                  isOnline ? 'bg-emerald-500' : 'bg-rose-500'
                }`}
              />
              {isOnline ? 'System Online' : 'System Offline'}
            </div>
          </header>

          <div className="p-6">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  )
}