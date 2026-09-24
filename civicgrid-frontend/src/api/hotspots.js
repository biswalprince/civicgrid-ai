import api from './axios'

export async function getHotspots() {
  const response = await api.get('api/hotspots/')
  return response.data
}