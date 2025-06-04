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
import {getUserId} from "./services/api.js";
import AuthCallbackPage from "./components/AuthCallback/AuthCallback.jsx";

function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  )
}

function AppContent() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)
  const location = useLocation()

  useEffect(() => {
    const checkAuth = () => {
      const userId = getUserId()
      setIsAuthenticated(!!userId)
      setLoading(false)
    }

    checkAuth()

    const handleStorageChange = () => checkAuth()
    window.addEventListener('storage', handleStorageChange)

    return () => {
      window.removeEventListener('storage', handleStorageChange)
    }
  }, [location])

  if (loading) return <div>Loading...</div>

  return (
    <Routes>
      <Route
        path="/"
        element={isAuthenticated ? <Navigate to="/competitions" replace /> : <LoginPage />}
      />

      <Route element={isAuthenticated ? <Layout /> : <Navigate to="/" replace />}>
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
        <Route path="/auth-callback" element={<AuthCallbackPage />} />
      </Route>

      <Route path="*" element={isAuthenticated ? <div>404 Not Found</div> : <Navigate to="/" replace />} />
    </Routes>
  )
}

export default App