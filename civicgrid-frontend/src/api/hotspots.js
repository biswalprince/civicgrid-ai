import api from './axios'

export async function getHotspots() {
  const response = await api.get('/hotspots/')
  return response.data
}