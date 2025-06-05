import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import CompetitionPreview from '../../components/CompetitionPreview/CompetitionPreview.jsx'
import { fetchCompetitions } from '../../services/api'
import styles from './CompetitionsPage.module.css'

// Главная страница ленты соревнований
export default function CompetitionsPage() {
  const [competitions, setCompetitions] = useState([])
  const [loading, setLoading] = useState(true)

  // Загружаем соревнования при монтировании компонента
  useEffect(() => {
    const loadCompetitions = async () => {
      try {
        // Получаем данные о соревнованиях с сервера
        const data = await fetchCompetitions()
        setCompetitions(data)
      } catch (error) {
        // Обработка ошибок загрузки
        console.error('Error loading competitions:', error)
      } finally {
        setLoading(false)
      }
    }
    loadCompetitions()
  }, [])

  return (
    // Основной контейнер страницы
    <div className={styles.page}>
      <div className={styles.header}>
        <h1 className={styles.title}>Лента соревнований</h1>
        <div className={styles.controls}>
          <Link to="/my_competitions" className={styles.button}>
            Мои соревнования
          </Link>
          <Link to="/competitions_constructor" className={styles.button}>
            Добавить соревнование
          </Link>
        </div>
      </div>

      {/* Список соревнований или индикатор загрузки */}
      {loading ? (
        <div>Loading competitions...</div>
      ) : (
        <div className={styles.list}>
          {competitions.map(competition => (
            <CompetitionPreview
              key={competition.id}
              {...competition}
            />
          ))}
        </div>
      )}
    </div>
  )
}