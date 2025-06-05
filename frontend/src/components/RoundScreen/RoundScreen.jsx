import { useState, useEffect } from 'react';
import styles from './RoundScreen.module.css';
import RoundIndicator from "../RoundIndicator/RoundIndicator.jsx";
import ScoreBoard from "../ScoreBoard/ScoreBoard.jsx";

/**
 * Компонент экрана раунда, отображает:
 * - Таймер раунда
 * - Индикатор прогресса раундов
 * - Задачи раунда с вариантами ответов
 * - Кнопку отправки ответов
 */
export default function RoundScreen({
  roundData,
  onSubmit,
  totalRounds,
  currentRound,
  roundResults,
  scores = { user: 0, opponent: 0, status: 'default'}
}) {
  const [answers, setAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState(roundData.time_limit);

  // Таймер обратного отсчета для раунда
  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  // Обработчик изменения ответов
  const handleAnswerChange = (problemId, value) => {
    setAnswers(prev => ({
      ...prev,
      [problemId]: Array.isArray(value) ? value : [value]
    }));
  };

  return (
    <div className={styles.roundContainer}>

      <ScoreBoard
        userScore={scores.user}
        opponentScore={scores.opponent}
        status={scores.status}
      />
      <div className={styles.timer}>Осталось времени: {timeLeft} сек.</div>
      <RoundIndicator
        total={totalRounds}
        current={currentRound}
        results={roundResults}
      />

      {roundData.problems.map(problem => (
        <div key={problem.id} className={styles.problemCard}>
          <h3>{problem.name}</h3>
          <p>{problem.text}</p>

          {/* Варианты ответов для одиночного выбора */}
          {problem.task_type === 'single choice' && (
            <div className={styles.options}>
              {problem.value.answers.map((answer, index) => (
                <label key={index}>
                  <input
                    type="radio"
                    name={`problem-${problem.id}`}
                    onChange={() => handleAnswerChange(problem.id, answer)}
                  />
                  {answer}
                </label>
              ))}
            </div>
          )}

          {/* Варианты ответов для множественного выбора */}
          {problem.task_type === 'multiple choice' && (
            <div className={styles.options}>
              {problem.value.answers.map((answer, index) => (
                <label key={index}>
                  <input
                    type="checkbox"
                    onChange={(e) => {
                      const newAnswers = e.target.checked
                        ? [...(answers[problem.id] || []), answer]
                        : (answers[problem.id] || []).filter(a => a !== answer);
                      handleAnswerChange(problem.id, newAnswers);
                    }}
                  />
                  {answer}
                </label>
              ))}
            </div>
          )}

          {/* Поле ввода для строкового ответа */}
          {problem.task_type === 'string' && (
            <div>
              <input
                type="text"
                onChange={(e) => handleAnswerChange(problem.id, e.target.value)}
                className={styles.textInput}
              />
              <p className={styles.hint}>Введите строку</p>
            </div>
          )}

          {/* Поле ввода для числового ответа */}
          {problem.task_type === 'number' && (
            <div>
              <input
                type="text"
                onChange={(e) => {
                  const value = e.target.value;
                  const numberValue = parseFloat(value);
                  handleAnswerChange(problem.id, isNaN(numberValue) ? '' : numberValue);
                }}
                className={styles.textInput}
              />
              <p className={styles.hint}>Дробные числа вводите через точку, например: 3.14</p>
            </div>
          )}
        </div>
      ))}

      <button
        onClick={() => onSubmit(answers)}
        className={styles.submitButton}
        disabled={timeLeft === 0}
      >
        {timeLeft > 0 ? 'Отправить ответы' : 'Время вышло!'}
      </button>
    </div>
  );
}