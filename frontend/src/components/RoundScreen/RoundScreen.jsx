import { useState, useEffect } from 'react';
import styles from './RoundScreen.module.css';

export default function RoundScreen({ roundData, onSubmit }) {
  const [answers, setAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState(roundData.time_limit);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const handleAnswerChange = (problemId, value) => {
    setAnswers(prev => ({
      ...prev,
      [problemId]: Array.isArray(value) ? value : [value]
    }));
  };

  return (
    <div className={styles.roundContainer}>
      <div className={styles.timer}>Осталось времени: {timeLeft} сек.</div>

      {roundData.problems.map(problem => (
        <div key={problem.id} className={styles.problemCard}>
          <h3>{problem.name}</h3>
          <p>{problem.text}</p>

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

          {['string', 'int'].includes(problem.task_type) && (
            <input
              type="text"
              onChange={(e) => handleAnswerChange(problem.id, e.target.value)}
              className={styles.textInput}
            />
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