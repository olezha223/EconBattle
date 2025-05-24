import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import styles from './LoginPage.module.css'


export default function LoginPage() {
  const navigate = useNavigate()

  useEffect(() => {
    const handleLogin = async () => {
      try {
        // Открываем окно авторизации
        window.open(
            'http://econ-battle.ru/api/login',
            '_blank',
            'width=500,height=600'
        )

        window.addEventListener('message', (event) => {
          if (!['http://econ-battle.ru', 'http://frontend:5173'].includes(event.origin)) return

          if (event.data.user) {
            localStorage.setItem('user_id', event.data.user.sub)
            localStorage.setItem('username', event.data.user.name)
            window.location.href = '/competitions'
          }
        }, false)
      } catch (error) {
        console.error('Login failed:', error)
      }
    }
    handleLogin()
  }, [navigate])

  return <div className={styles.container}>Redirecting to login...</div>
}