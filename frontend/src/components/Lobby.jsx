import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useWebsocket } from '../contexts/WebsocketContext';

export default function Lobby() {
  const [username, setUsername] = useState('');
  const navigate = useNavigate();
  const { sendMessage } = useWebsocket();

  const handleFindMatch = () => {
    if (!username.trim()) return;

    sendMessage(JSON.stringify({
      type: 'join_queue',
      username: username.trim()
    }));

    navigate('/game');
  };

  return (
    <div className="lobby">
      <h1>Введите имя</h1>
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Ваше имя"
      />
      <button onClick={handleFindMatch}>
        Найти игру
      </button>
    </div>
  );
}