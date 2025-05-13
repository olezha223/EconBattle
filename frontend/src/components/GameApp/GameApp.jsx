import {useEffect, useRef, useState} from 'react';
import { useParams } from 'react-router-dom';
import styles from './GameApp.module.css';
import RoundScreen from '../RoundScreen/RoundScreen.jsx';
import ResultsScreen from "../ResultsScreen/ResultsScreen.jsx";

const getUserId = () => localStorage.getItem('user_id') || '';

export default function GameApp() {
  const { competition_id } = useParams();
  const [socket, setSocket] = useState(null);
  const [gameState, setGameState] = useState('connecting');
  const [roundData, setRoundData] = useState(null);
  const [results, setResults] = useState(null);
  const [opponent, setOpponent] = useState('');
  const [gameResult, setGameResult] = useState(null);
  const [totalRounds, setTotalRounds] = useState(0);
  const [roundResults, setRoundResults] = useState([]);
  const [currentRound, setCurrentRound] = useState(0);

  const currentRoundRef = useRef(currentRound);
  currentRoundRef.current = currentRound;

  useEffect(() => {
    const ws = new WebSocket(
      `ws://localhost:8000/ws/?user_id=${getUserId()}&competition_id=${competition_id}`
    );

    const calculateResult = (userScore, opponentScore) => {
      if (userScore > opponentScore) return 'win';
      if (userScore < opponentScore) return 'lose';
      return 'draw';
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      switch (data.type) {
        case 'connected':
          setGameState('waiting');
          break;

        case 'waiting':
          setGameState('waiting');
          break;

        case 'matched':
          setOpponent(data.msg.split(': ')[1]);
          setGameState('matched');
          setTimeout(() => setGameState('round'), 3000);
          break;

        case 'Game':
          setTotalRounds(data.round_count);
          setRoundResults(Array(data.round_count).fill(null));
          setCurrentRound(0);
          break;

        case 'Start Round':
          setRoundData(data);
          setGameState('round');
          setCurrentRound(prev => prev + 1);
          break;

        case 'round_result': {
          const userId = getUserId();
          const opponentId = Object.keys(data.scores).find(id => id !== userId);

          const result = calculateResult(
            data.scores[userId],
            data.scores[opponentId]
          );

          setRoundResults(prev => {
            const newResults = [...prev];
            newResults[currentRoundRef.current - 1] = result;
            return newResults;
          });

          setResults(data);
          setGameState('results');
          break;
        }

        case 'game_end':
          setGameResult(data);
          setGameState('game_end');
          ws.close();
          break;

        default:
          console.warn('Unknown message type:', data.type);
      }
    };

    setSocket(ws);

    return () => {
      ws.close();
      setSocket(null);
    }
  }, [competition_id]); // Только competition_id в зависимостях

  const handleAnswersSubmit = (answers) => {
    socket.send(JSON.stringify({
      type: 'answers',
      answers: answers
    }));
    setGameState('awaiting_opponent');
  };

  return (
    <div className={styles.container}>
      {gameState === 'connecting' && <div>Подключение...</div>}

      {gameState === 'waiting' && (
        <div className={styles.waiting}>
          Ожидаем соперника...
        </div>
      )}

      {gameState === 'matched' && (
        <div className={styles.matched}>
          Соперник найден! Информация о нем: {opponent}
        </div>
      )}

      {gameState === 'round' && (
        <RoundScreen
          roundData={roundData}
          onSubmit={handleAnswersSubmit}
          totalRounds={totalRounds}
          currentRound={currentRound}
          roundResults={roundResults}
        />
      )}

      {gameState === 'awaiting_opponent' && (
        <div className={styles.waiting}>
          Ожидаем ответа соперника...
          <div className={styles.loader}></div>
        </div>
      )}

      {gameState === 'results' && (
        <ResultsScreen
          results={results}
          totalRounds={totalRounds}
          currentRound={currentRound}
          roundResults={roundResults}
          onContinue={() => setGameState('waiting')}
        />
      )}

      {gameState === 'game_end' && (
        <div className={styles.endScreen}>
          <h2>Игра завершена!</h2>
          <p>Результат: {gameResult.status}</p>
          <p>Счет: {gameResult.final_scores[getUserId()]}</p>
          <a href="/" className={styles.button}>На главную</a>
        </div>
      )}
    </div>
  );
}