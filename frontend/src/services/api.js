import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  withCredentials: true
})

// Функция для получения айди пользователя
export const getUserId = () => localStorage.getItem('user_id')

export const fetchUserTasks = async () => {
  const userId = getUserId()
  const response = await api.get('/tasks/previews', {
    params: { user_id: userId },
    withCredentials: true
  })
  return response.data
}

// Получить превью публичных задач, которые создал пользователь
export const fetchPreviews = async (userId) => {
  const response = await api.get('/tasks/previews-public', {
    params: { user_id: userId },
    withCredentials: true
  })
  return response.data
}

// Получить превью соревнований, которые создал пользователь
export const fetchUserCompetitions = async (userId) => {
  const response = await api.get('/competitions/previews', {
    params: { user_id: userId },
    withCredentials: true
  })
  return response.data
}

// Получить превью всех задач из банка платформы
export const fetchAllTasks = async () => {
  const response = await api.get('/tasks/all', {withCredentials: true })
  return response.data
}

// Получить превью всех соревнований из банка платформы
export const fetchCompetitions = async () => {
  const response = await api.get('/competitions/all', {withCredentials: true })
  return response.data
}

// Получить детальную информацию о соревновании
export const fetchCompetitionDetails = async (competitionId) => {
  const response = await api.get('/competitions/', {
    params: { competition_id: competitionId },
    withCredentials: true
  })
  return response.data
}

// Получить ссылку на аватарку пользователя в гугле
export const fetchPictureUrl = async () => {
  const response = await api.get(`/users/picture`, {
    params: { user_id: getUserId() },
    withCredentials: true
  });
  return response.data;
};

// Получить детальную статистику пользователя на платформе
export const fetchUserInfo = async (userId) => {
  const response = await api.get('/users/info', {
    params: { user_id: userId },
    withCredentials: true
  })
  return response.data
}

// Получить детальную информацию о задаче
export const fetchTaskDetails = async (taskId) => {
  const response = await api.get('/tasks/', {
    params: { task_id: taskId },
    withCredentials: true
  })
  return response.data
}

// Создать задачу
export const createTask = async (taskData) => {
  const response = await api.post('/tasks/', taskData, {withCredentials: true });
  return response.data;
};

// Обновить имя пользователя
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

// Получить все задачи (в том числе и приватные) для текущего пользователя
export const fetchUserTasksPreviews = async () => {
  const response = await api.get('/tasks/previews', {
    params: { user_id: getUserId() },
    withCredentials: true
  });
  return response.data;
};

// Создать соревнование
export const createCompetition = async (competitionData) => {
  const response = await api.post('/competitions/', competitionData, {
    withCredentials: true
  });
  return response.data;
};