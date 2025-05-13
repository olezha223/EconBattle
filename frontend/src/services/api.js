import axios from 'axios'

export const getUserId = () => localStorage.getItem('user_id')

export const fetchUserTasks = async () => {
  const userId = getUserId()
  const response = await api.get('/tasks/previews', {
    params: { user_id: userId }
  })
  return response.data
}

export const fetchPreviews = async (userId) => {
  const response = await api.get('/tasks/previews-public', {
    params: { user_id: userId }
  })
  return response.data
}

export const fetchUserCompetitions = async (userId) => {
  const response = await api.get('/competitions/previews', {
    params: { user_id: userId }
  })
  return response.data
}

export const fetchAllTasks = async () => {
  const response = await api.get('/tasks/all')
  return response.data
}
const api = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true
})

export const fetchCompetitions = async () => {
  const response = await api.get('/competitions/all')
  return response.data
}

export const createUser = async (userData) => {
  return api.post('/user', null, {
    params: {
      user_id: userData.sub,
      username: userData.name
    }
  })
}

export const fetchCompetitionDetails = async (competitionId) => {
  const response = await api.get('/competitions/', {
    params: { competition_id: competitionId }
  })
  return response.data
}

