import api from './axios'

export async function getInfrastructureIndicators(params) {
  const response = await api.get('/infrastructure-indicators/', { params })
  return response.data
}