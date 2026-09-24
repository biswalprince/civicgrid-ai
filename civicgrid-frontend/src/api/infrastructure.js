import api from './axios'

export async function getInfrastructureIndicators(params) {
  const response = await api.get('/api/infrastructure-indicators/', { params })
  return response.data
}