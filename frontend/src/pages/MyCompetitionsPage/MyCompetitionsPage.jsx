import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import CompetitionPreview from '../../components/CompetitionPreview/CompetitionPreview';
import { getUserId } from '../../services/api';
import axios from 'axios';
import styles from './MyCompetitionsPage.module.css';

const API_URL = 'http://localhost:8000';

export default function MyCompetitionsPage() {
  const [competitions, setCompetitions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchCompetitions = async () => {
      try {
        const userId = getUserId();
        if (!userId) throw new Error('User not authenticated');

        const response = await axios.get(
          `${API_URL}/competitions/previews`,
          {
            params: { user_id: userId },
            withCredentials: true
          }
        );

        setCompetitions(response.data);
      } catch (err) {
        setError(err.response?.data?.detail || 'Ошибка загрузки соревнований');
      } finally {
        setLoading(false);
      }
    };

    fetchCompetitions();
  }, []);

  // Остальная часть компонента без изменений
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