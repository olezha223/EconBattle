import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { fetchCompetitionDetails } from '../../services/api'
import styles from './CompetitionDetailsPage.module.css'

export default function CompetitionDetailsPage() {
  const { id } = useParams()
  const [competition, setCompetition] = useState(null)
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

  if (loading) return <div>Loading...</div>
  if (!competition) return <div>Competition not found</div>

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>{competition.name}</h1>

      <div className={styles.grid}>
        <div className={styles.item}>
          <span className={styles.label}>Создатель:</span>
          <span className={styles.value}>{competition.creator_id}</span>
        </div>

        <div className={styles.item}>
          <span className={styles.label}>Макс. игроков:</span>
          <span className={styles.value}>{competition.max_players}</span>
        </div>

        <div className={styles.item}>
          <span className={styles.label}>Макс. раундов:</span>
          <span className={styles.value}>{competition.max_rounds}</span>
        </div>

        <div className={styles.item}>
          <span className={styles.label}>Время раунда:</span>
          <span className={styles.value}>
            {competition.round_time_in_seconds} сек.
          </span>
        </div>

        <div className={styles.item}>
          <span className={styles.label}>Создано:</span>
          <span className={styles.value}>
            {new Date(competition.created_at).toLocaleDateString()}
          </span>
        </div>
      </div>

      <button className={styles.button}>
        Начать!
      </button>
    </div>
  )
}