import styles from './ResultsScreen.module.css';

export default function ResultsScreen({ results }) {
  return (
    <div className={styles.resultsContainer}>
      <h2>Результаты раунда</h2>
      <div className={styles.scores}>
        {Object.entries(results.scores).map(([userId, score]) => (
          <div key={userId}>
            Игрок {userId}: {score} очков
          </div>
        ))}
      </div>
    </div>
  );
}