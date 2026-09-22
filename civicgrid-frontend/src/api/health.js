import api from './axios'

export async function checkHealth() {
  const response = await api.get('/health/')
  return response.data
}