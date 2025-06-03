import { Link } from 'react-router-dom';
import styles from './UserProfile.module.css';
import ActivityGrid from '../ActivityGrid/ActivityGrid';

const UserProfile = ({ userData }) => {
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
            <span>На платформе с</span>
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
            'Средняя сложность': userData.mean_task_difficulty
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