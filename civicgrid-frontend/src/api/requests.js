import api from './axios'

export async function getRequests(params) {
  const response = await api.get('/api/requests/', { params })
  return response.data
}

export async function createRequest(description) {
  const response = await api.post('/api/requests/', {
    description,
  })
  return response.data
}