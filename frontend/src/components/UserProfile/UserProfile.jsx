import { Link } from 'react-router-dom';
import styles from './UserProfile.module.css';

// профиль пользователя (не текущего)
const UserProfile = ({ userData }) => {
  // Активность
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

  // Блок со статистикой
  const StatsBlock = ({ title, stats, links }) => (
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
      {links.map((link, index) => (
        <Link
          key={index}
          to={link.to}
          className={styles.statsButton}
        >
          {link.label}
        </Link>
      ))}
    </div>
  </div>
);

  return (
    <div className={styles.container}>
      <div className={styles.profileHeader}>
        <img
          src={userData.picture}
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
            <span>На платформе с</span>
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
          title="Статистика игр"
          stats={{
            'Победы': userData.wins_count,
            'Поражения': userData.losses_count,
            'Ничьи': userData.tie_count,
            'Всего игр': userData.games_played
          }}
          links={[
            {
              label: 'Найти соревнование',
              to: '/competitions'
            }
          ]}
        />

        <StatsBlock
          title="Созданный контент"
          stats={{
            'Создано задач': userData.tasks_created,
            'Создано соревнований': userData.competitions_created,
            'Средняя сложность': userData.mean_task_difficulty,
            'Сколько раз игроки решали задачи': userData.tasks_popularity_count
          }}
          links={[
            {
              label: 'Просмотреть задачи',
              to: `/user_tasks/${userData?.id}`
            },
            {
              label: 'Просмотреть соревнования',
              to: `/user_competitions/${userData?.id}`
            }
          ]}
        />
      </div>
    </div>
  );
};

export default UserProfile;