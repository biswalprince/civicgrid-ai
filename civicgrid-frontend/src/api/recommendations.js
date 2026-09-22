import api from './axios'

export async function generateRecommendation(id) {
  const response = await api.post(`/requests/${id}/recommend/`)
  return response.data
}