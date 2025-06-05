import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import TaskPreview from '../../components/TaskPreview/TaskPreview.jsx'
import { fetchUserTasks, getUserId } from '../../services/api'
import styles from './MyTasksPage.module.css'

// Компонент страницы "Мои задачи". Отображает список соревнований пользователя, а также кнопки для перехода к банку и созданию нового.
export default function MyTasksPage() {
  const [myTasks, setMyTasks] = useState([])
  const [loading, setLoading] = useState(true)

  // Загрузка данных
  useEffect(() => {
    const loadData = async () => {
      try {
        const userId = getUserId()
        if (!userId) throw new Error('User not authenticated')

        const data = await fetchUserTasks()
        setMyTasks(data)
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
        <h1 className={styles.title}>Мои задачи</h1>
        <div className={styles.controls}>
          <Link to="/tasks" className={styles.button}>
            Банк задач
          </Link>
          <Link to="/tasks_constructor" className={styles.button}>
            Добавить задачу
          </Link>
        </div>
      </div>

      <div className={styles.list}>
        {myTasks.map(task => (
          <TaskPreview key={task.id} {...task} />
        ))}
        {myTasks.length === 0 && (
          <div className={styles.empty}>
            <p>У вас пока нет созданных задач</p>
            <Link to="/tasks_constructor" className={styles.button}>
              Создать первую задачу
            </Link>
          </div>
        )}
      </div>
    </div>
  )
}