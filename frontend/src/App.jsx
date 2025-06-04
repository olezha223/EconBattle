import {BrowserRouter, Routes, Route, Navigate, useLocation} from 'react-router-dom'
import { useState, useEffect } from 'react'
import CompetitionsPage from './pages/CompetitionsPage/CompetitionsPage.jsx'
import LoginPage from './pages/LoginPage/LoginPage.jsx'
import CompetitionDetailsPage from './pages/CompetitionDetailsPage/CompetitionDetailsPage.jsx'
import TasksPage from './pages/TasksPage/TasksPage.jsx'
import TaskConstructorPage from './pages/TaskConstructorPage/TaskConstructorPage.jsx'
import Layout from './components/Layout/Layout.jsx'
import TaskDetailsPage from './pages/TaskDetailsPage/TaskDetailsPage.jsx'
import ProfilePage from "./pages/ProfilePage/ProfilePage.jsx";
import MyTasksPage from "./pages/MyTasksPage/MyTasksPage.jsx";
import CompetitionConstructorPage from "./pages/CompetitionConstructorPage/CompetitionConstructorPage.jsx";
import MyCompetitionsPage from "./pages/MyCompetitionsPage/MyCompetitionsPage.jsx";
import UserPage from "./pages/UserPage/UserPage.jsx";
import UserTasksPage from "./pages/TasksPage/UserTasksPage.jsx";
import UserCompetitionsPage from "./pages/CompetitionsPage/UserCompetitionsPage.jsx";
import GameApp from "./components/GameApp/GameApp.jsx";
import AuthSuccessPage from "./pages/AuthSuccessPage/AuthSuccessPage.jsx";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)
  const location = useLocation()

  useEffect(() => {
    const checkAuth = () => {
      const userId = localStorage.getItem('user_id')
      setIsAuthenticated(!!userId)
      setLoading(false)
    }

    // Проверяем аутентификацию при монтировании и при изменении пути
    checkAuth()

    // Синхронизация между вкладками
    const handleStorage = () => {
      const userId = localStorage.getItem('user_id')
      setIsAuthenticated(!!userId)
    }
    window.addEventListener('storage', handleStorage)
    return () => window.removeEventListener('storage', handleStorage)
  }, [])

  useEffect(() => {
    const userId = localStorage.getItem('user_id')
    setIsAuthenticated(!!userId)
  }, [location.pathname])

  if (loading) return <div>Loading...</div>

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={isAuthenticated ? <Navigate to="/competitions" replace /> : <LoginPage />}
        />

        <Route path="/auth-success" element={<AuthSuccessPage setIsAuthenticated={setIsAuthenticated} />} />

        <Route element={<ProtectedRoute isAuthenticated={isAuthenticated}><Layout /></ProtectedRoute>}>
          <Route path="competitions" element={<CompetitionsPage />} />
          <Route path="competitions/:id" element={<CompetitionDetailsPage />} />
          <Route path="competitions_constructor" element={<CompetitionConstructorPage />} />
          <Route path="user_page/:userId" element={<UserPage />} />
          <Route path="tasks" element={<TasksPage />} />
          <Route path="tasks/:id" element={<TaskDetailsPage />} />
          <Route path="tasks_constructor" element={<TaskConstructorPage />} />
          <Route path="profile" element={<ProfilePage />} />
          <Route path="my_tasks" element={<MyTasksPage />} />
          <Route path="my_competitions" element={<MyCompetitionsPage />} />
          <Route path="user_tasks/:userId" element={<UserTasksPage />} />
          <Route path="user_competitions/:userId" element={<UserCompetitionsPage />} />
          <Route path="game/:competition_id" element={<GameApp />} />
          <Route path="/auth-success" element={<AuthSuccessPage />} />
        </Route>

        <Route path="*" element={isAuthenticated ? <div>404 Not Found</div> : <Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

const ProtectedRoute = ({ isAuthenticated, children }) => {
  const location = useLocation()

  if (!isAuthenticated) {
    return <Navigate to={`/?redirect=${encodeURIComponent(location.pathname)}`} replace />
  }
  return children
}

export default App