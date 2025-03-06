// src/pages/GamePage.jsx
import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

export default function GamePage() {
  const [problems, setProblems] = useState([]);
  const [timeLeft, setTimeLeft] = useState(180);
  const location = useLocation();
  const navigate = useNavigate();
  const gameId = new URLSearchParams(location.search).get('game_id');
  const [ws, setWs] = useState(null);

  useEffect(() => {
    const username = localStorage.getItem('username'); // Нужно сохранять username при входе
    const newWs = new WebSocket(`ws://localhost:8000/ws?username=${username}`);

    newWs.onmessage = (event) => {
      const data = JSON.parse(event.data);
      switch (data.type) {
        case 'start_round':
          setProblems(data.problems);
          setTimeLeft(data.time_limit);
          break;
        case 'opponent_disconnected':
          alert('Соперник отключился!');
          navigate('/');
          break;
      }
    };

    setWs(newWs);

    return () => {
      newWs.close();
    };
  }, [gameId, navigate]);

  return (
    <div>
      <div>Время: {timeLeft} сек</div>
      <div className="problems-container">
        {problems.map((problem) => (
          <div key={problem.id} className="problem-card">
            <h3>Вопрос: {problem.question_text}</h3>
            <div className="answers">
              {Object.entries(problem.answers).map(([key, value]) => (
                <button key={key} onClick={() => handleAnswer(problem.id, key)}>
                  {value}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}