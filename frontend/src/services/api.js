import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  withCredentials: true
})

export const getUserId = () => localStorage.getItem('user_id')

export const fetchUserTasks = async () => {
  const userId = getUserId()
  const response = await api.get('/tasks/previews', {
    params: { user_id: userId },
    withCredentials: true
  })
  return response.data
}

export const fetchPreviews = async (userId) => {
  const response = await api.get('/tasks/previews-public', {
    params: { user_id: userId },
    withCredentials: true
  })
  return response.data
}

export const fetchUserCompetitions = async (userId) => {
  const response = await api.get('/competitions/previews', {
    params: { user_id: userId },
    withCredentials: true
  })
  return response.data
}

export const fetchAllTasks = async () => {
  const response = await api.get('/tasks/all', {withCredentials: true })
  return response.data
}

export const fetchCompetitions = async () => {
  const response = await api.get('/competitions/all', {withCredentials: true })
  return response.data
}

export const fetchCompetitionDetails = async (competitionId) => {
  const response = await api.get('/competitions/', {
    params: { competition_id: competitionId },
    withCredentials: true
  })
  return response.data
}

export const fetchPictureUrl = async () => {
  const response = await api.get(`/users/picture`, {
    params: { user_id: getUserId() },
    withCredentials: true
  });
  return response.data;
};


export const fetchUserInfo = async (userId) => {
  const response = await api.get('/users/info', {
    params: { user_id: userId },
    withCredentials: true
  })
  return response.data
}

export const fetchTaskDetails = async (taskId) => {
  const response = await api.get('/tasks/', {
    params: { task_id: taskId },
    withCredentials: true
  })
  return response.data
}

export const createTask = async (taskData) => {
  const response = await api.post('/tasks/', taskData, {withCredentials: true });
  return response.data;
};

export const updateUsername = async (userId, newUsername) => {
  const response = await api.put('/users/update_username', null, {
    params: {
      user_id: userId,
      username: newUsername
    },
    headers: {
      'accept': 'application/json'
    },
    withCredentials: true
  })
  return response.data
}

export const fetchUserTasksPreviews = async () => {
  const response = await api.get('/tasks/previews', {
    params: { user_id: getUserId() },
    withCredentials: true
  });
  return response.data;
};

export const createCompetition = async (competitionData) => {
  const response = await api.post('/competitions/', competitionData, {
    withCredentials: true
  });
  return response.data;
};