import { useEffect, useState } from 'react';

function RoundScreen({ problems, answers, setAnswers, websocket }) {
  const [hasSent, setHasSent] = useState(false);

  const handleAnswerChange = (index, value) => {
    const newAnswers = [...answers];
    newAnswers[index] = value;
    setAnswers(newAnswers);
  };

  useEffect(() => {
    if (
      !hasSent &&
      problems &&
      answers.length === problems.length &&
      answers.every((a) => a !== '')
    ) {
      websocket.send(JSON.stringify({ answers }));
      setHasSent(true);
    }
  }, [answers, problems, hasSent, websocket]);

  return (
    <div className="round-screen">
      <h2 className="round-title">Раунд</h2>
      <div className="problems-list">
        {problems.map((problem, index) => (
          <div key={index} className="problem-item">
            <p className="problem-question">
              Задача {index + 1}: {problem.question}
            </p>
            <input
              type="text"
              value={answers[index] || ''}
              onChange={(e) => handleAnswerChange(index, e.target.value)}
              placeholder="Введите ответ"
              className="answer-input"
            />
          </div>
        ))}
      </div>
    </div>
  );
}

export default RoundScreen;