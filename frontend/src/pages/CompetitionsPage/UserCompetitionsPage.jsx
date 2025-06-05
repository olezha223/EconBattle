import { useState, useEffect } from 'react'
import { Link, useParams } from 'react-router-dom'
import CompetitionPreview from '../../components/CompetitionPreview/CompetitionPreview.jsx'
import { fetchUserCompetitions } from '../../services/api'
import styles from './CompetitionsPage.module.css'

// Страница соревнований конкретного пользователя
export default function UserCompetitionsPage() {
  const [competitions, setCompetitions] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  // Получаем userId из параметров маршрута
  const { userId } = useParams()

  // Загружаем соревнования пользователя при изменении userId
  useEffect(() => {
    const loadCompetitions = async () => {
      try {
        // Получаем данные о соревнованиях пользователя с сервера
        const data = await fetchUserCompetitions(userId)

        // Гарантируем, что data всегда будет массивом
        if (!Array.isArray(data)) {
          throw new Error('Некорректный формат данных')
        }

        setCompetitions(data)
        setError(null)
      } catch (error) {
        console.error('Ошибка загрузки:', error)
        setError(error.message)
        setCompetitions([]) // Сбрасываем до пустого массива
      } finally {
        setLoading(false)
      }
    }

    loadCompetitions()
  }, [userId])

  return (
    // Основной контейнер страницы
    <div className={styles.page}>
      <div className={styles.header}>
        <h1 className={styles.title}>Соревнования пользователя</h1>
        <div className={styles.controls}>
          <Link to="/competitions" className={styles.button}>
            Все соревнования
          </Link>
        </div>
      </div>

      {/* Список соревнований, индикатор загрузки или сообщение об ошибке */}
      {loading ? (
        <div>Загрузка соревнований...</div>
      ) : error ? (
        <div className={styles.error}>Ошибка: {error}</div>
      ) : (
        <div className={styles.list}>
          {competitions.length > 0 ? (
            competitions.map(competition => (
              <CompetitionPreview
                key={competition.id}
                {...competition}
              />
            ))
          ) : (
            <div className={styles.empty}>Соревнований не найдено</div>
          )}
        </div>
      )}
    </div>
  )
}