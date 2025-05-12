import { useState, useEffect } from 'react'
import RoundScreen from "../RoundScreen/RoundScreen.jsx";
import "./GameScreen.module.css"

function GameScreen({ gameState, opponent, playerId, sendMessage, lastMessage }) {
  const [roundData, setRoundData] = useState(null);
  const [timer, setTimer] = useState(0);
  const [isRoundActive, setIsRoundActive] = useState(false);

  useEffect(() => {
    if (lastMessage) {
      try {
        const message = JSON.parse(lastMessage.data);

        if (message.type === 'Start Round') {
          setRoundData({
            problems: message.problems,
            time_limit: message.time_limit
          });
          setTimer(message.time_limit);
          setIsRoundActive(true);
        }
      } catch (e) {
        console.error('Error parsing message:', e);
      }
    }
  }, [lastMessage]);

  useEffect(() => {
    let interval;
    if (isRoundActive && timer > 0) {
      interval = setInterval(() => {
        setTimer(prev => prev - 1);
      }, 1000);
    } else if (timer === 0) {
      setIsRoundActive(false);
    }
    return () => clearInterval(interval);
  }, [isRoundActive, timer]);

  const handleAnswersSubmit = (answers) => {
    sendMessage({
      type: 'answers',
      data: answers
    });
    setIsRoundActive(false);
  };

  return (
    <div className="game-container">
      {gameState === 'waiting' && (
        <div className="waiting-message">
          <h2>Waiting for opponent...</h2>
          <p>Please wait while we find you a match</p>
        </div>
      )}

      {gameState === 'game' && (
        <>
          <div className="game-header">
            <div className="player-info">
              <span className="player-name">{playerId}</span>
              <span className="vs-text">vs</span>
              <span className="opponent-name">{opponent}</span>
            </div>
            <div className="timer">
              ⏳ {Math.floor(timer / 60)}:{(timer % 60).toString().padStart(2, '0')}
            </div>
          </div>

          {isRoundActive && roundData?.problems && (
            <RoundScreen
              problems={roundData.problems}
              onSubmit={handleAnswersSubmit}
              timeLeft={timer}
            />
          )}
        </>
      )}
    </div>
  )
}

export default GameScreen