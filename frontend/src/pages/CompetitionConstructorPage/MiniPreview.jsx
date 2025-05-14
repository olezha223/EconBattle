import { formatTimeAgo } from '../../utils/timeUtils';
import styles from './CompetitionConstructorPage.module.css';

export default function MiniPreview({ task, onSelect }) {
  return (
    <div className={styles.miniPreview} onClick={() => onSelect(task.id)}>
      <h4>{task.name}</h4>
      <div className={styles.stats}>
        <div className={styles.stat}>
          <span className={styles.label}>Сложность:</span>
          <span className={styles.value}>{task.price}</span>
        </div>
        <div className={styles.stat}>
          <span className={styles.label}>Создано:</span>
          <span className={styles.value}>
            {formatTimeAgo(new Date(task.created_at))}
          </span>
        </div>
      </div>
    </div>
  )
}