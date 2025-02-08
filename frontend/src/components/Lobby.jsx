import { useNavigate } from 'react-router-dom';
import { useWebSocketContext } from '../contexts/WebSocketContext';
import { useEffect } from 'react';
import { Button } from '@mui/material';

export default function Lobby() {
  const navigate = useNavigate();
  const { sendMessage, lastMessage } = useWebSocketContext();

  useEffect(() => {
    if (lastMessage?.data) {
      const data = JSON.parse(lastMessage.data);
      if (data.type === 'match_found') navigate('/game');
    }
  }, [lastMessage, navigate]);

  return (
    <div>
      <h1>Найти игру</h1>
      <Button
        variant="contained"
        onClick={() => sendMessage(JSON.stringify({ type: 'find_match' }))}
      >
        Играть
      </Button>
    </div>
  );
}