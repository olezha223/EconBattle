import styles from './ResultsScreen.module.css';
import RoundIndicator from "../RoundIndicator/RoundIndicator.jsx";

export default function ResultsScreen({
  results,
  totalRounds,
  currentRound,
  roundResults
}) {
  return (
    <div className={styles.resultsContainer}>
      <h2>Результаты раунда</h2>

      <RoundIndicator
        total={totalRounds}
        current={currentRound}
        results={roundResults}
      />

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