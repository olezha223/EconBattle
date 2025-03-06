// src/pages/HomePage.jsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function HomePage() {
  const [username, setUsername] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [ws, setWs] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!username) return;

    const newWs = new WebSocket(`ws://localhost:8000/ws?username=${username}`);
    setWs(newWs);
    setIsSearching(true);

    newWs.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'matched') {
        navigate(`/game?game_id=${data.game_id}`);
      }
    };

    newWs.onclose = () => {
      setIsSearching(false);
      setWs(null);
    };
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Введите имя"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          disabled={isSearching}
        />
        <button type="submit" disabled={isSearching}>
          {isSearching ? 'Поиск...' : 'Найти соперника'}
        </button>
      </form>
    </div>
  );
}