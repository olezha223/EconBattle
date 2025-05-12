import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './ProfilePage.module.css';

const API_URL = 'http://localhost:8000';

export default function ProfilePage() {
  const navigate = useNavigate();
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const userId = localStorage.getItem('user_id');
        const response = await axios.get(`${API_URL}/users/info?user_id=${userId}`, {
          withCredentials: true
        });
        setUserData(response.data);
      } catch (err) {
        setError('Ошибка загрузки данных профиля');
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  const renderActivityGrid = () => {
    if (!userData?.user_activity) return null;

    // Получаем и сортируем все даты
    const dates = Object.keys(userData.user_activity)
      .sort((a, b) => new Date(a) - new Date(b));

    // Создаем матрицу недель
    const weeks = [];
    let currentWeek = [];

    dates.forEach(date => {
      const day = new Date(date).getDay(); // 0-6 (воскресенье-суббота)
      const adjustedDay = day === 0 ? 6 : day - 1; // преобразуем к 0-6 (понедельник-воскресенье)

      if (adjustedDay === 0 && currentWeek.length > 0) {
        weeks.push(currentWeek);
        currentWeek = [];
      }

      currentWeek[adjustedDay] = {
        date,
        activity: userData.user_activity[date]
      };
    });

    if (currentWeek.length > 0) weeks.push(currentWeek);

    // Находим максимальную активность для цветов
    const maxActivity = Math.max(...Object.values(userData.user_activity));

    return (
      <div className={styles.activityContainer}>
        {/* Легенда дней недели */}
        <div className={styles.weekDaysLegend}>
          {['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'].map((day, index) => (
            <div key={index} className={styles.weekDay}>{day}</div>
          ))}
        </div>

        {/* Сетка активности */}
        <div className={styles.weeksGrid}>
          {weeks.map((week, weekIndex) => (
            <div key={weekIndex} className={styles.weekColumn}>
              {Array(7).fill().map((_, dayIndex) => {
                const dayData = week[dayIndex];
                const activity = dayData?.activity || 0;
                const intensity = activity > 0 ? activity / maxActivity : 0;

                return (
                  <div
                    key={dayIndex}
                    className={styles.dayCell}
                    data-tooltip={dayData ?
                      `${new Date(dayData.date).toLocaleDateString('ru-RU')}: ${activity} активностей` :
                      'Нет данных'}
                  >
                    <div
                      className={styles.activitySquare}
                      style={{
                        backgroundColor: activity > 0
                          ? `rgba(46, 160, 67, ${0.2 + intensity * 0.8})`
                          : '#ebedf0'
                      }}
                    />
                  </div>
                );
              })}
            </div>
          ))}
        </div>
      </div>
    );
  };

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

  if (loading) return <div className={styles.loading}>Загрузка...</div>;
  if (error) return <div className={styles.error}>{error}</div>;

  return (
    <div className={styles.container}>
      <div className={styles.profileHeader}>
        <img
          src="/static/default-avatar.jpg"
          alt="Аватар"
          className={styles.profileAvatar}
        />
        <h1>{userData.username}</h1>
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
        {renderActivityGrid()}
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