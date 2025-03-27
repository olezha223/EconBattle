import { useState, useEffect } from 'react'
import RoundScreen from './RoundScreen'
import '../styles/GameScreen.css'

function GameScreen({ ws, gameState, opponent, playerId }) {
  const [roundData, setRoundData] = useState(null)
  const [timer, setTimer] = useState(0)
  const [isRoundActive, setIsRoundActive] = useState(false)

  useEffect(() => {
    if (!ws) return

    const messageHandler = (event) => {
      const message = JSON.parse(event.data)
      if (message.type === 'Start Round') {
        setRoundData({
          problems: message.problems,
          time_limit: message.time_limit
        })
        setTimer(message.time_limit)
        setIsRoundActive(true)
      }
    }

    ws.addEventListener('message', messageHandler)
    return () => ws.removeEventListener('message', messageHandler)
  }, [ws])

  // Таймер и логика игры
  useEffect(() => {
    let interval
    if (isRoundActive) {
      interval = setInterval(() => {
        setTimer(prev => prev > 0 ? prev - 1 : 0)
      }, 1000)
    }
    return () => clearInterval(interval)
  }, [isRoundActive])

  const handleAnswersSubmit = (answers) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ answers }))
      setIsRoundActive(false)
    }
  }

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
            <h2>Your opponent: {opponent}</h2>
            {isRoundActive && <div className="timer">Time left: {timer}s</div>}
          </div>

          {roundData && isRoundActive && (
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