import styles from './ResultsScreen.module.css';
import RoundIndicator from "../RoundIndicator/RoundIndicator.jsx";
import ScoreBoard from "../ScoreBoard/ScoreBoard.jsx";

export default function ResultsScreen({
  results,
  totalRounds,
  currentRound,
  roundResults,
  currentScores = { user: 0, opponent: 0 }
}) {
  return (
    <div className={styles.resultsContainer}>
      <h2>Результаты раунда</h2>

      <ScoreBoard
        userScore={currentScores.user}
        opponentScore={currentScores.opponent}
      />

      <RoundIndicator
        total={totalRounds}
        current={currentRound}
        results={roundResults}
      />

      <div className={styles.scores}>
        {results?.scores && Object.entries(results.scores).map(([userId, score]) => (
          <div key={userId}>
            Игрок {userId}: {score} очков
          </div>
        ))}
      </div>
    </div>
  );
}