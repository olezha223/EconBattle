import { useState, useEffect } from 'react'
import { Link, useParams } from 'react-router-dom'
import TaskPreview from '../../components/TaskPreview/TaskPreview.jsx'
import {fetchPreviews} from '../../services/api'
import styles from './TasksPage.module.css'


// основной компонент страницы задач пользователя
export default function UserTasksPage() {
  const [userTasks, setUserTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const { userId } = useParams()

  // загрузка данных
  useEffect(() => {
    const loadData = async () => {
      try {
        const data = await fetchPreviews(userId)
        setUserTasks(data)
      } catch (error) {
        console.error('Error loading user tasks:', error)
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [userId])

  if (loading) return <div>Loading...</div>

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <h1 className={styles.title}>Задачи пользователя</h1>
        <div className={styles.controls}>
          <Link to="/tasks" className={styles.button}>
            Все задачи
          </Link>
        </div>
      </div>

      <div className={styles.list}>
        {userTasks.map(task => (
          <TaskPreview key={task.id} {...task} />
        ))}
      </div>
    </div>
  )
}