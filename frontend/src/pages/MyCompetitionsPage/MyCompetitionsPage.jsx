import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import CompetitionPreview from '../../components/CompetitionPreview/CompetitionPreview';
import {fetchUserCompetitions, getUserId} from '../../services/api';
import styles from './MyCompetitionsPage.module.css';

// Компонент страницы "Мои соревнования". Отображает список соревнований пользователя, а также кнопки для перехода к банку соревнований и созданию нового.
export default function MyCompetitionsPage() {
  const [competitions, setCompetitions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    // Асинхронная функция для загрузки соревнований пользователя
    const fetchCompetitions = async () => {
      try {
        const userId = getUserId()
        if (!userId) throw new Error('User not authenticated')

        // Загружаем соревнования пользователя с сервера
        const data = await fetchUserCompetitions(userId)
        setCompetitions(data)
      } catch (err) {
        // Обработка ошибок загрузки
        setError(err.response?.data?.detail || 'Ошибка загрузки соревнований')
      } finally {
        setLoading(false)
      }
    }

    fetchCompetitions()
  }, [])

  if (loading) return <div className={styles.loading}>Загрузка...</div>;
  if (error) return <div className={styles.error}>{error}</div>;

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <h1 className={styles.title}>Мои соревнования</h1>
        <div className={styles.controls}>
          <Link to="/competitions" className={styles.button}>
            Банк соревнований
          </Link>
          <Link to="/competitions_constructor" className={styles.button}>
            Создать соревнование
          </Link>
        </div>
      </div>

      <div className={styles.list}>
        {/* Если есть соревнования — отображаем их список */}
        {competitions.length > 0 ? (
          competitions.map(competition => (
            <CompetitionPreview key={competition.id} {...competition} />
          ))
        ) : (
          <div className={styles.empty}>
            <p>У вас пока нет созданных соревнований</p>
            <Link to="/competitions_constructor" className={styles.button}>
              Создать первое соревнование
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}