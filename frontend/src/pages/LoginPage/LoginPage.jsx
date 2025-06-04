import { useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import styles from './LoginPage.module.css'


export default function LoginPage() {
  const [searchParams] = useSearchParams()

  useEffect(() => {
    const error = searchParams.get('error')

    if (error) {
      alert(`Authentication error: ${error}`)
    }
  }, [searchParams])

  const handleLogin = () => {
    const redirectPath = searchParams.get('redirect') || '/competitions'
    window.location.href = `http://econ-battle.ru/api/login?redirect_after=${encodeURIComponent(redirectPath)}`
  }

  return (
    <div className={styles.container}>
      <button onClick={handleLogin} className={styles.loginButton}>
        Login with Google
      </button>
    </div>
  )
}