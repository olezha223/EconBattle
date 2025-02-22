// components/Game.jsx
import { useEffect, useState } from 'react';
import { useWebsocket } from '../contexts/WebsocketContext';
import { useNavigate } from 'react-router-dom';
import { ReadyState } from 'react-use-websocket';

export default function Game() {
  const { lastMessage, readyState } = useWebsocket();
  const navigate = useNavigate();
  const [gameState, setGameState] = useState({
    status: 'waiting', // waiting, playing, finished
    problems: [],
    timeLeft: 0,
    score: 0,
    opponent: null
  });

  // Обработка изменения состояния соединения
  useEffect(() => {
    if (readyState === ReadyState.CLOSED) {
      alert('Соединение с сервером потеряно!');
      navigate('/');
    }
  }, [readyState, navigate]);

  // Обработка входящих сообщений
  useEffect(() => {
    if (!lastMessage?.data) return;

    const data = JSON.parse(lastMessage.data);

    switch(data.type) {
      case 'round_start':
        setGameState({
          ...gameState,
          status: 'playing',
          problems: data.problems,
          timeLeft: data.time_left,
          opponent: data.opponent
        });
        break;

      case 'timer_update':
        setGameState(prev => ({
          ...prev,
          timeLeft: data.time_left
        }));
        break;

      case 'round_result':
        setGameState(prev => ({
          ...prev,
          status: 'round_result',
          score: data.your_score,
          opponentScore: data.opponent_score
        }));
        break;

      case 'game_over':
        setGameState(prev => ({
          ...prev,
          status: 'finished',
          score: data.final_score,
          isWinner: data.is_winner
        }));
        break;
    }
  }, [lastMessage]);

  // Отправка ответов
  const handleAnswerSubmit = (problemId, answer) => {
    const { sendMessage } = useWebsocket();
    sendMessage(JSON.stringify({
      type: 'submit_answer',
      problem_id: problemId,
      answer: answer
    }));
  };

  return (
    <div className="game-container">
      {gameState.status === 'waiting' && (
        <div className="waiting-screen">
          <h2>Поиск соперника...</h2>
          <p>Пожалуйста, подождите</p>
        </div>
      )}

      {gameState.status === 'playing' && (
        <>
          <div className="game-header">
            <h3>Соперник: {gameState.opponent?.username || 'Неизвестный'}</h3>
            <div className="timer">
              Осталось времени: {gameState.timeLeft} сек
            </div>
          </div>

          <div className="problems-list">
            {gameState.problems.map((problem, index) => (
              <div key={index} className="problem-card">
                <h4>Вопрос {index + 1}</h4>
                <p>{problem.question}</p>
                <input
                  type="number"
                  placeholder="Ваш ответ"
                  onChange={(e) =>
                    handleAnswerSubmit(problem.id, e.target.value)
                  }
                />
              </div>
            ))}
          </div>
        </>
      )}

      {gameState.status === 'round_result' && (
        <div className="round-result">
          <h2>Результаты раунда</h2>
          <p>Ваш счет: {gameState.score}</p>
          <p>Счет соперника: {gameState.opponentScore}</p>
        </div>
      )}

      {gameState.status === 'finished' && (
        <div className="game-over">
          <h2>Игра завершена!</h2>
          <p>Финальный счет: {gameState.score}</p>
          <p>{gameState.isWinner ? '🎉 Вы победили!' : '😢 Вы проиграли'}</p>
          <button onClick={() => navigate('/')}>
            Вернуться в лобби
          </button>
        </div>
      )}
    </div>
  );
}