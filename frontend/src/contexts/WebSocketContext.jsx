// contexts/WebsocketContext.jsx
import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';

const WebsocketContext = createContext(null);

export const WebsocketProvider = ({ children }) => {
  const [socketUrl] = useState('ws://localhost:8000/ws');
  const [shouldReconnect, setShouldReconnect] = useState(true);
  const [messageHistory, setMessageHistory] = useState([]);

  // Параметры подключения
  const { sendMessage, lastMessage, readyState, getWebSocket } = useWebSocket(
    socketUrl,
    {
      shouldReconnect: () => shouldReconnect,
      reconnectInterval: 3000,
      reconnectAttempts: 5,
      onReconnectStop: () => {
        setShouldReconnect(false);
        alert('Не удалось подключиться к серверу');
      },
    }
  );

  // Состояние подключения
  const connectionStatus = {
    [ReadyState.CONNECTING]: 'Подключение',
    [ReadyState.OPEN]: 'Подключено',
    [ReadyState.CLOSING]: 'Закрытие',
    [ReadyState.CLOSED]: 'Отключено',
  }[readyState];

  // Обработка входящих сообщений
  useEffect(() => {
    if (lastMessage !== null) {
      setMessageHistory((prev) => prev.concat(lastMessage));
    }
  }, [lastMessage]);

  // Автоматическое восстановление подключения
  useEffect(() => {
    if (readyState === ReadyState.CLOSED && shouldReconnect) {
      const ws = getWebSocket();
      ws?.reconnect();
    }
  }, [readyState, shouldReconnect]);

  // Значение контекста
  const contextValue = useMemo(() => ({
    sendMessage,
    lastMessage,
    messageHistory,
    readyState,
    connectionStatus,
    disconnect: () => {
      setShouldReconnect(false);
      getWebSocket()?.close();
    },
    reconnect: () => {
      setShouldReconnect(true);
      getWebSocket()?.reconnect();
    },
  }), [sendMessage, lastMessage, messageHistory, readyState]);

  return (
    <WebsocketContext.Provider value={contextValue}>
      {children}
    </WebsocketContext.Provider>
  );
};

export const useWebsocket = () => {
  const context = useContext(WebsocketContext);
  if (!context) {
    throw new Error('useWebsocket must be used within WebsocketProvider');
  }
  return context;
};