// Верхнеуровневый компонент App.jsx
import { useState, useEffect } from 'react'
import GameScreen from './components/GameScreen'
import LobbyScreen from './components/LobbyScreen'
import './styles/index.css'

function App() {
  const [gameState, setGameState] = useState('lobby')
  const [opponent, setOpponent] = useState(null)
  const [playerId, setPlayerId] = useState('')
  const [ws, setWs] = useState(null)

  // Общий обработчик сообщений
  useEffect(() => {
    if (!ws) return

    const messageHandler = (event) => {
      const message = JSON.parse(event.data)
      switch(message.type) {
        case 'matched':
          setOpponent(message.msg.split(': ')[1])
          setGameState('game')
          break
        case 'Start Round':
          // Обработка начала раунда
          break
        case 'Closing':
          ws.close()
          break
      }
    }

    ws.addEventListener('message', messageHandler)
    return () => ws.removeEventListener('message', messageHandler)
  }, [ws])

  // Обработчик закрытия соединения
  useEffect(() => {
    if (!ws) return

    const closeHandler = () => {
      setGameState('lobby')
      setWs(null)
    }

    ws.addEventListener('close', closeHandler)
    return () => ws.removeEventListener('close', closeHandler)
  }, [ws])

  return (
    <div className="app-container">
      {gameState === 'lobby' && (
        <LobbyScreen 
          onConnect={(id) => {
            const newWs = new WebSocket(`ws://localhost:8000/ws/${id}`)
            newWs.onopen = () => {
              setPlayerId(id)
              setGameState('waiting')
              setWs(newWs)
            }
          }}
        />
      )}
      
      {(gameState === 'waiting' || gameState === 'game') && (
        <GameScreen 
          ws={ws}
          gameState={gameState}
          opponent={opponent}
          playerId={playerId}
        />
      )}
    </div>
  );
}

export default App;