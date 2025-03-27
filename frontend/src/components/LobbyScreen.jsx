// components/LobbyScreen.jsx
import { useState } from 'react'
import '../styles/LobbyScreen.css'

function LobbyScreen({ onConnect }) {
  const [name, setName] = useState('')

  const handleStartGame = () => {
    if (name.trim()) {
      onConnect(name)
    }
  }

  return (
    <div className="lobby-container">
      <h1>Math Game</h1>
      <div className="input-group">
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Enter your name"
        />
        <button onClick={handleStartGame} disabled={!name.trim()}>
          Find Opponent
        </button>
      </div>
    </div>
  )
}

export default LobbyScreen