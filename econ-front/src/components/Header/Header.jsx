import { Link } from 'react-router-dom'
import styles from './Header.module.css'

export default function Header() {
  return (
    <header className={styles.header}>
      <div className={styles.logo}>
        <Link to="/competitions">Math Competitions</Link>
      </div>

      <nav className={styles.nav}>
        <Link to="/profile" className={styles.profileLink}>
          <img
            src="/static/default-avatar.jpg"
            alt="Profile"
            className={styles.avatar}
          />
        </Link>
      </nav>
    </header>
  )
}