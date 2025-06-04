import styles from './LoginPage.module.css'


export default function LoginPage() {
  const handleLogin = () => {
    window.location.href = 'http://econ-battle.ru/api/login'
  }

  return (
    <div className={styles.container}>
      <button onClick={handleLogin} className={styles.loginButton}>
        Login with Google
      </button>
    </div>
  )
}