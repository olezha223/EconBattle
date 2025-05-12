import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import GameScreen from '../../components/GameScreen/GameScreen.jsx';
import useWebSocket from '../../hooks/useWebSocket';
import './GameApp.module.css'

function GameApp() {
  const { competition_id } = useParams();
  const navigate = useNavigate();
  const [gameState, setGameState] = useState('waiting'); // Начальное состояние изменено на waiting
  const [opponent, setOpponent] = useState(null);
  const [playerId, setPlayerId] = useState('');
  const [roundResults, setRoundResults] = useState([]);
  const [gameResult, setGameResult] = useState(null);
  const userId = localStorage.getItem('user_id');

  const wsUrl = `ws://localhost:8000/ws/?user_id=${userId}&competition_id=${competition_id}`;
  const { sendMessage, lastMessage } = useWebSocket(wsUrl);

  useEffect(() => {
    // Автоматически подключаемся при монтировании компонента
    setPlayerId(userId);
  }, [userId]);

  useEffect(() => {
    if (lastMessage) {
      const message = JSON.parse(lastMessage.data);
      switch(message.type) {
        case 'matched':
          setOpponent(message.msg.split(': ')[1]);
          setGameState('game');
          break;
        case 'Start Round':
          setGameState('game');
          break;
        case 'round_result':
          setRoundResults(prev => [...prev, message]);
          break;
        case 'game_end':
          setGameResult(message);
          setGameState('finished');
          break;
        case 'Closing':
          navigate('/competitions');
          break;
      }
    }
  }, [lastMessage, navigate]);

  return (
    <div className="app-container">
      {gameState === 'waiting' && (
        <GameScreen
          gameState={gameState}
          opponent={opponent}
          playerId={playerId}
          sendMessage={sendMessage}
        />
      )}

      {gameState === 'game' && (
        <GameScreen
          gameState={gameState}
          opponent={opponent}
          playerId={playerId}
          sendMessage={sendMessage}
          lastMessage={lastMessage}
        />
      )}

      {gameState === 'finished' && gameResult && (
        <div className="result-container">
          <h2>Игра завершена!</h2>
          <p>Статус: {gameResult.status}</p>
          <p>Счёт: {gameResult.final_scores[userId]}</p>
          <button
            onClick={() => navigate('/competitions')}
            className="return-button"
          >
            Вернуться к соревнованиям
          </button>
        </div>
      )}
    </div>
  );
}

export default GameApp;