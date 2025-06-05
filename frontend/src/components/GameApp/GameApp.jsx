import {useEffect, useRef, useState} from 'react';
import { useParams } from 'react-router-dom';
import styles from './GameApp.module.css';
import RoundScreen from '../RoundScreen/RoundScreen.jsx';
import ResultsScreen from "../ResultsScreen/ResultsScreen.jsx";
import ScoreBoard from "../ScoreBoard/ScoreBoard.jsx";
import {getUserId} from "../../services/api.js";
import Opponent from "../Opponent/Opponent.jsx";

export default function GameApp() {
  const { competition_id } = useParams();
  const [socket, setSocket] = useState(null);
  const shouldWarnOnUnloadRef = useRef(true);
  const [gameState, setGameState] = useState('connecting');
  const [roundData, setRoundData] = useState(null);
  const [results, setResults] = useState(null);
  const [opponent, setOpponent] = useState(null);
  const [gameResult, setGameResult] = useState(null);
  const [totalRounds, setTotalRounds] = useState(0);
  const [roundResults, setRoundResults] = useState([]);
  const [currentRound, setCurrentRound] = useState(0);
  const [currentScores, setCurrentScores] = useState({
    user: 0,
    opponent: 0,
    status: 'default',
  });
  const [finalScores, setFinalScores] = useState({ user: 0, opponent: 0 });
  const [waitingTime, setWaitingTime] = useState(60);
  const timerRef = useRef(null);
  const statusMap = {
      'winner': { text: 'ПОБЕДА!', color: '#40c057' },
      'loser': { text: 'ПОРАЖЕНИЕ', color: '#fa5252' },
      'tie': { text: 'НИЧЬЯ', color: '#ffd43b' }
  };

  const currentRoundRef = useRef(currentRound);
  currentRoundRef.current = currentRound;

  const startWaitingTimer = () => {
    setWaitingTime(60);
    if (timerRef.current) {
      clearInterval(timerRef.current);
    }
    timerRef.current = setInterval(() => {
      setWaitingTime(prev => {
        if (prev <= 1) {
          clearInterval(timerRef.current);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  const connectToGame = () => {
    const ws = new WebSocket(
      `wss://econ-battle.ru/api/ws/?user_id=${getUserId()}&competition_id=${competition_id}`
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
          startWaitingTimer();
          break;

        case 'waiting':
          setGameState('waiting');
          startWaitingTimer();
          break;

        case 'search time limit reached':
          setGameState('no_opponent');
          if (timerRef.current) {
            clearInterval(timerRef.current);
          }
          break;

        case 'matched':
          setOpponent(data.msg);
          setGameState('matched');
          if (timerRef.current) {
            clearInterval(timerRef.current);
          }
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

          setCurrentScores({
            user: data.total_score[userId],
            opponent: data.total_score[opponentId],
            status: data.statuses[userId]
          });

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

        case 'game_end': {
          const userId = getUserId();
          const opponentId = Object.keys(data.final_scores).find(id => id !== userId);
          setFinalScores({
            user: data.final_scores[userId],
            opponent: data.final_scores[opponentId]
          });

          setGameResult(data);
          shouldWarnOnUnloadRef.current = false;
          setGameState('game_end');
          ws.close();
          break;
        }

        default:
          console.warn('Unknown message type:', data.type);
      }
    };

    setSocket(ws);
    return ws;
  };

  useEffect(() => {
    const ws = connectToGame();

    const handleBeforeUnload = (e) => {
      if (shouldWarnOnUnloadRef.current) {
        e.preventDefault();
        e.returnValue = '';
        if (ws && ws.readyState === WebSocket.OPEN) {
          try {
            ws.send(JSON.stringify({ type: 'user exit' }));
          } catch (err) {console.log(err)}
        }
        return '';
      }
    };
    window.addEventListener('beforeunload', handleBeforeUnload);

    return () => {
      if (ws && ws.readyState === WebSocket.OPEN) {
        try {
          ws.send(JSON.stringify({ type: 'user exit' }));
        } catch (err) {console.log(err)}
        ws.close();
      }

      setSocket(null);
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
      window.removeEventListener('beforeunload', handleBeforeUnload);
    }
  }, [competition_id]);

  const handleRetry = () => {
    if (socket) {
      socket.close();
    }
    connectToGame();
  };

  const handleAnswersSubmit = (answers) => {
    socket.send(JSON.stringify({
      type: 'answers',
      answers: answers
    }));
    setGameState('awaiting_opponent');
  };

  const renderGameResultHeader = () => {
    if (!gameResult) return null;

    const { text, color } = statusMap[gameResult.status] || { text: 'Игра завершена', color: '#666' };

    return <h2 style={{ color, fontSize: '3rem', margin: '20px 0' }}>{text}</h2>;
  };

  const renderRatingInfo = () => {
    if (!gameResult) return null;

    const { new_rating, diff } = gameResult;
    // Форматируем разницу со знаком
    const formattedDiff = diff > 0 ? `+${diff}` : diff;

    return (
      <p className={styles.ratingInfo}>
        Рейтинг студента: {new_rating} (
        <span style={{ color: statusMap[gameResult.status] }}>{formattedDiff}</span>
        )
      </p>
    );
  };

  return (
    <div className={styles.container}>
      {gameState === 'connecting' && (
        <div>Подключение..., При долгом ожидании, обновите страницу.</div>
      )}

      {gameState === 'waiting' && (
        <div className={styles.waiting}>
          <div>Ожидаем соперника...</div>
          <div className={styles.timer}>Осталось времени: {waitingTime} сек</div>
        </div>
      )}

      {gameState === 'no_opponent' && (
        <div className={styles.noOpponent}>
          <h2>Не удалось найти соперника</h2>
          <p>К сожалению, за отведенное время не удалось найти подходящего соперника.</p>
          <button onClick={handleRetry} className={styles.button}>
            Попробовать снова
          </button>
        </div>
      )}

      {gameState === 'matched' && (
        <div className={styles.matched}>
          <h2 className={styles.matchedTitle}>Соперник найден!</h2>
          <Opponent opponent={opponent} />
        </div>
      )}

      {gameState === 'round' && (
        <RoundScreen
          roundData={roundData}
          onSubmit={handleAnswersSubmit}
          totalRounds={totalRounds}
          currentRound={currentRound}
          roundResults={roundResults}
          scores={currentScores}
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
          currentScores={currentScores}
          onContinue={() => setGameState('waiting')}
        />
      )}

      {gameState === 'game_end' && (
        <div className={styles.endScreen}>
          {renderGameResultHeader()}
          <ScoreBoard
            userScore={finalScores.user}
            opponentScore={finalScores.opponent}
            status={gameResult.status}
          />
          <div className={styles.finalStats}>
            {renderRatingInfo()}
          </div>
          <a href="/" className={styles.button}>На главную</a>
        </div>
      )}
    </div>
  );
}