import styles from './ScoreBoard.module.css';

export default function ScoreBoard({ userScore, opponentScore, status}) {
  return (
    <div className={`${styles.scoreContainer} ${styles[status]}`}>
      <div className={styles.scoreItem}>
        <span className={styles.scoreLabel}>Ваш счет</span>
        <span className={styles.scoreValue}>{userScore}</span>
      </div>
      <div className={styles.scoreSeparator}>:</div>
      <div className={styles.scoreItem}>
        <span className={styles.scoreLabel}>Счет соперника</span>
        <span className={styles.scoreValue}>{opponentScore}</span>
      </div>
    </div>
  );
}