import { useState, useEffect } from 'react'
import { useNavigate, useParams, Link } from 'react-router-dom' // Добавили Link
import { fetchCompetitionDetails } from '../../services/api'
import styles from './CompetitionDetailsPage.module.css'

export default function CompetitionDetailsPage() {
  const { id } = useParams()
  const [competition, setCompetition] = useState(null)
  const navigate = useNavigate()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadCompetition = async () => {
      try {
        const data = await fetchCompetitionDetails(id)
        setCompetition(data)
      } catch (error) {
        console.error('Error loading competition:', error)
      } finally {
        setLoading(false)
      }
    }
    loadCompetition()
  }, [id])

  const handleStartGame = () => {
    navigate(`/game/${id}`)
  }

  const handleAuthorClick = (e) => {
    e.stopPropagation()
  }

  if (loading) return <div>Loading...</div>
  if (!competition) return <div>Competition not found</div>

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>{competition.name}</h1>

      <div className={styles.grid}>
        <div className={styles.item}>
          <span className={styles.label}>Создатель:</span>
          <div className={styles.value}>
            <Link
              to={`/user_page/${competition.creator_id}`}
              className={styles.creatorLink}
              onClick={handleAuthorClick}
            >
              <img
                src={competition.picture}
                alt="Аватар автора"
                className={styles.creatorAvatar}
              />
              <span>{competition.creator_name}</span>
            </Link>
          </div>
        </div>

        <div className={styles.item}>
          <span className={styles.label}>Число раундов:</span>
          <span className={styles.value}>{competition.max_rounds}</span>
        </div>

        <div className={styles.item}>
          <span className={styles.label}>Максимальная длительность игры:</span>
          <span className={styles.value}>
            {competition.max_time} сек.
          </span>
        </div>

        <div className={styles.item}>
          <span className={styles.label}>Создано:</span>
          <span className={styles.value}>
            {new Date(competition.created_at).toLocaleDateString()}
          </span>
        </div>

        <div className={styles.item}>
          <span className={styles.label}>Средняя сложность задач:</span>
          <span className={styles.value}>{competition.mean_task_difficulty}</span>
        </div>

        <div className={styles.item}>
          <span className={styles.label}>Процент правильно решенных задач в игре:</span>
          <span className={styles.value}>{competition.percent_of_correct}%</span>
        </div>
      </div>

      <button className={styles.button} onClick={handleStartGame}>
        Начать!
      </button>
    </div>
  )
}