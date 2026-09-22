import { BrowserRouter, Route, Routes } from 'react-router-dom'
import AppLayout from './components/layout/AppLayout'
import Dashboard from './pages/Dashboard'
import Requests from './pages/Requests'
import RequestDetails from './pages/RequestDetails'
import Hotspots from './pages/Hotspots'
import Infrastructure from './pages/Infrastructure'
import Recommendations from './pages/Recommendations'

function PlaceholderPage({ title }) {
  return (
    <section>
      <p className="text-sm font-medium text-blue-600">CivicGrid AI</p>
      <h1 className="mt-2 text-3xl font-semibold text-slate-900">{title}</h1>
      <p className="mt-3 text-slate-600">This decision-support view is being prepared.</p>
    </section>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/requests" element={<Requests />} />
          <Route path="/requests/:id" element={<RequestDetails />} />
          <Route path="/hotspots" element={<Hotspots />} />
          <Route path="/infrastructure" element={<Infrastructure />} />
          <Route path="/recommendations" element={<Recommendations />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}