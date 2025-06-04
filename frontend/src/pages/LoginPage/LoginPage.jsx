import { useSearchParams } from 'react-router-dom'
import styles from './LoginPage.module.css'
import GoogleIcon from './GoogleIcon'

export default function LoginPage() {
  const [searchParams] = useSearchParams()

  const handleLogin = () => {
    const redirectPath = searchParams.get('redirect') || '/competitions'
    window.location.href = `http://econ-battle.ru/api/login?redirect_after=${encodeURIComponent(redirectPath)}`
  }

  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <h1 className={styles.title}>Добро пожаловать!</h1>
        <p className={styles.description}>
          Это приложение для преподавателей и студентов для отработки навыков решения задач по экономическим моделям.
        </p>

        <button onClick={handleLogin} className={styles.loginButton}>
          <GoogleIcon className={styles.googleIcon} />
          <span>Войти через Google</span>
        </button>

        <p className={styles.contact}>
          По всем вопросам можно написать на почту <br />
          <a href="mailto:oashvetsov@edu.hse.ru">oashvetsov@edu.hse.ru</a>
        </p>
      </div>
    </div>
  )
}