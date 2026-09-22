import api from './axios'

export async function getRequests(params) {
  const response = await api.get('/requests/', { params })
  return response.data
}