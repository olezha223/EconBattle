import { createContext, useContext } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';

const WebSocketContext = createContext(null);

export const WebSocketProvider = ({ children }) => {
  const handleMessage = (data) => {
    // Глобальная обработка сообщений
    console.log('Received message:', data);
  };

  const { send } = useWebSocket(
    'ws://localhost:8000/ws',
    handleMessage
  );

  return (
    <WebSocketContext.Provider value={{ send }}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocketContext = () => useContext(WebSocketContext);