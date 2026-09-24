import api from './axios'

export async function getRequests(params) {
  const response = await api.get('/api/requests/', { params })
  return response.data
}