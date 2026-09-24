import api from './axios'

export async function getDashboardSummary() {
  const response = await api.get('/api/dashboard/summary/')
  return response.data
}