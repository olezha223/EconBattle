import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import TaskPreview from '../../components/TaskPreview/TaskPreview.jsx'
import { fetchAllTasks } from '../../services/api'
import styles from './TasksPage.module.css'

// основной компонент страницы банка задач
export default function TasksPage() {
  const [bankTasks, setBankTasks] = useState([])
  const [loading, setLoading] = useState(true)

  // загрузка данных
  useEffect(() => {
    const loadData = async () => {
      try {
        const data = await fetchAllTasks()
        setBankTasks(data)
      } catch (error) {
        console.error('Error loading tasks:', error)
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [])

  if (loading) return <div>Loading...</div>

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <h1 className={styles.title}>Банк задач</h1>
        <div className={styles.controls}>
          <Link to="/my_tasks" className={styles.button}>
            Мои задачи
          </Link>
          <Link to="/tasks_constructor" className={styles.button}>
            Добавить задачу
          </Link>
        </div>
      </div>

      <div className={styles.list}>
        {bankTasks.map(task => (
          <TaskPreview key={task.id} {...task} />
        ))}
      </div>
    </div>
  )
}