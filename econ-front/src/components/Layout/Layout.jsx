import { Link, Outlet } from 'react-router-dom'
import Header from '../Header/Header.jsx'
import styles from './Layout.module.css'

export default function Layout() {
  return (
    <div className={styles.layout}>
      <Header />
      <nav className={styles.mainNav}>
        <Link to="/competitions">Соревнования</Link>
        <Link to="/tasks">Задачи</Link>
      </nav>
      <div className={styles.content}>
        <Outlet />
      </div>
    </div>
  )
}