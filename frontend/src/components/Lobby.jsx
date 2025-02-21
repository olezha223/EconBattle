// components/Lobby.jsx
import { useState, useEffect } from 'react';
import { useWebSocketContext } from '../contexts/WebSocketContext';
import { useNavigate } from 'react-router-dom';

export default function Lobby() {
  const { sendMessage, connect } = useWebSocketContext();
  const navigate = useNavigate();
  const [isConnecting, setIsConnecting] = useState(false);

  useEffect(() => {
    const wsUrl = `ws://localhost:8000/ws`;
    connect(wsUrl); // Подключаемся к WebSocket
  }, [connect, navigate]);

  const handleStartGame = () => {
    if (isConnecting) return;

    setIsConnecting(true);
    sendMessage({ type: 'find_match' }); // Отправляем сообщение
  };

  return (
    <div>
      <h1>Найти игру</h1>
      <button
        onClick={handleStartGame}
        disabled={isConnecting}
      >
        {isConnecting ? 'Поиск...' : 'Начать игру'}
      </button>
    </div>
  );
}