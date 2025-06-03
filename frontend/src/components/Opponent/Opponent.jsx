import styles from './Opponent.module.css';

export default function Opponent({ opponent }) {
  if (!opponent) return null;

  return (
    <div className={styles.container}>
      <div className={styles.avatarContainer}>
        <img
          src={opponent.picture || '/default-avatar.png'}
          alt={opponent.username}
          className={styles.avatar}
          onError={(e) => {
            e.target.onerror = null;
            e.target.src = '/default-avatar.png';
          }}
        />
        <div className={styles.statusIndicator}></div>
      </div>

      <div className={styles.info}>
        <h2 className={styles.username}>{opponent.username}</h2>

        <div className={styles.stats}>
          <div className={styles.stat}>
            <span className={styles.statLabel}>Рейтинг:</span>
            <span className={styles.statValue}>{opponent.student_rating}</span>
          </div>

          <div className={styles.stat}>
            <span className={styles.statLabel}>Рейтинг препод.:</span>
            <span className={styles.statValue}>{opponent.teacher_rating}</span>
          </div>
        </div>
      </div>
    </div>
  );
}