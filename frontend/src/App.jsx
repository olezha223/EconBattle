import { useState, useEffect } from 'react';
import LoginScreen from './components/LoginScreen';
import WaitingForOpponent from './components/WaitingForOpponent';
import RoundScreen from './components/RoundScreen';

function App() {
  const [gameState, setGameState] = useState('login');
  const [playerId, setPlayerId] = useState('');
  const [websocket, setWebsocket] = useState(null);
  const [opponentId, setOpponentId] = useState('');
  const [currentRound, setCurrentRound] = useState(null);
  const [answers, setAnswers] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!websocket) return;

    const handleMessage = (event) => {
      const data = JSON.parse(event.data);
      switch (data.type) {
        case 'connected':
          setGameState('waiting');
          break;
        case 'matched':
          const opponent = data.msg.split(': ')[1];
          setOpponentId(opponent);
          setGameState('matched');
          break;
        case 'Start Round':
          setCurrentRound({
            problems: data.problems,
            timeLimit: data.time_limit
          });
          setAnswers(Array(data.problems.length).fill(''));
          setGameState('round');
          break;
        case 'Closing':
          websocket.close();
          setGameState('closed');
          break;
        default:
          console.log('Unknown message type:', data.type);
      }
    };

    const handleError = (error) => {
      setError('Ошибка подключения');
    };

    const handleClose = () => {
      setGameState('closed');
    };

    websocket.addEventListener('message', handleMessage);
    websocket.addEventListener('error', handleError);
    websocket.addEventListener('close', handleClose);

    return () => {
      websocket.removeEventListener('message', handleMessage);
      websocket.removeEventListener('error', handleError);
      websocket.removeEventListener('close', handleClose);
    };
  }, [websocket]);

  const handleLogin = (enteredId) => {
    const ws = new WebSocket(`ws://localhost:8000/ws/${enteredId}`);
    setWebsocket(ws);
    setPlayerId(enteredId);
  };

  return (
    <div className="app">
      {gameState === 'login' && <LoginScreen onLogin={handleLogin} />}
      {gameState === 'waiting' && <WaitingForOpponent />}
      {gameState === 'matched' && (
        <WaitingForOpponent opponentId={opponentId} />
      )}
      {gameState === 'round' && (
        <RoundScreen
          problems={currentRound.problems}
          answers={answers}
          setAnswers={setAnswers}
          websocket={websocket}
        />
      )}
      {gameState === 'closed' && <div className="closed">Игра завершена</div>}
      {error && <div className="error">Ошибка: {error}</div>}
    </div>
  );
}

export default App;