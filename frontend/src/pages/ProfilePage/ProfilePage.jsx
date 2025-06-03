import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './ProfilePage.module.css';
import {fetchUserInfo, getUserId, updateUsername} from "../../services/api.js";
import ActivityGrid from '../../components/ActivityGrid/ActivityGrid';

export default function ProfilePage() {
  const navigate = useNavigate();
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [newUsername, setNewUsername] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const userId = getUserId();
        const data = await fetchUserInfo(userId);
        setUserData(data);
      } catch {
        setError('Ошибка загрузки данных профиля');
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  const StatsBlock = ({ title, stats, buttons }) => (
    <div className={styles.statsBlock}>
      <h3>{title}</h3>
      <div className={styles.statsContent}>
        {Object.entries(stats).map(([label, value]) => (
          <div key={label} className={styles.statItem}>
            <span className={styles.statLabel}>{label}</span>
            <span className={styles.statValue}>{value}</span>
          </div>
        ))}
      </div>
      <div className={styles.statsButtons}>
        {buttons.map((btn, index) => (
          <button
            key={index}
            className={styles.statsButton}
            onClick={btn.onClick}
          >
            {btn.label}
          </button>
        ))}
      </div>
    </div>
  );

  const handleUsernameUpdate = async () => {
    if (!newUsername.trim()) {
      setError('Имя не может быть пустым')
      return
    }

    try {
      await updateUsername(getUserId(), newUsername)
      setUserData(prev => ({ ...prev, username: newUsername }))
      setIsEditing(false)
      setError('')
    } catch (err) {
      setError(err.response?.data?.detail || 'Ошибка при изменении имени')
    }
  }

  if (loading) return <div className={styles.loading}>Загрузка...</div>;
  if (error) return <div className={styles.error}>{error}</div>;

  return (
    <div className={styles.container}>
      <div className={styles.profileHeader}>
        <img
          src={userData?.picture}
          alt="Аватар"
          className={styles.profileAvatar}
        />
        <div className={styles.nameContainer}>
          <h1>{userData?.username}</h1>
          <button
            onClick={() => {
              setIsEditing(true);
              setNewUsername(userData?.username);
            }}
            className={styles.editButton}
            aria-label="Изменить имя"
          >
            <svg className={styles.editIcon} viewBox="0 0 24 24">
              <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34a1.01 1.01 0 0 0-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
            </svg>
          </button>
        </div>

        {isEditing && (
          <div className={styles.modalOverlay}>
            <div className={styles.modal}>
              <h3>Изменить имя пользователя</h3>
              <input
                type="text"
                value={newUsername}
                onChange={(e) => setNewUsername(e.target.value)}
                className={styles.nameInput}
                maxLength={30}
              />
              <div className={styles.modalActions}>
                <button
                  onClick={handleUsernameUpdate}
                  className={styles.saveButton}
                >
                  Сохранить
                </button>
                <button
                  onClick={() => setIsEditing(false)}
                  className={styles.cancelButton}
                >
                  Отмена
                </button>
              </div>
            </div>
          </div>
        )}

        <div className={styles.profileInfo}>
          <div className={styles.infoItem}>
            <span>Рейтинг студента</span>
            <div className={styles.rating}>{userData.student_rating}</div>
          </div>
          <div className={styles.infoItem}>
            <span>Рейтинг преподавателя</span>
            <div className={styles.rating}>{userData.teacher_rating}</div>
          </div>
          <div className={styles.infoItem}>
            <span>Дата регистрации</span>
            <div className={styles.date}>
              {new Date(userData.created_at).toLocaleDateString()}
            </div>
          </div>
        </div>
      </div>

      <div className={styles.activitySection}>
        <h2>Активность</h2>
        <ActivityGrid userActivity={userData?.user_activity} />
      </div>

      <div className={styles.statsContainer}>
        <StatsBlock
          title="Статистика моих игр"
          stats={{
            'Победы': userData.wins_count,
            'Поражения': userData.losses_count,
            'Ничьи': userData.tie_count,
            'Всего игр': userData.games_played
          }}
          buttons={[
            {
              label: 'Найти соревнование',
              onClick: () => navigate('/competitions')
            }
          ]}
        />

        <StatsBlock
          title="Статистика задач и соревнований"
          stats={{
            'Создано задач': userData.tasks_created,
            'Создано соревнований': userData.competitions_created,
            'Средняя сложность': userData.mean_task_difficulty
          }}
          buttons={[
            {
              label: 'Мои задачи',
              onClick: () => navigate('/my_tasks')
            },
            {
              label: 'Мои соревнования',
              onClick: () => navigate('/my_competitions')
            }
          ]}
        />
      </div>
    </div>
  );
}