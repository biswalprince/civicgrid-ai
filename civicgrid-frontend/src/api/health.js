import api from './axios'

export async function checkHealth() {
  const response = await api.get('/api/health/')
  return response.data
}