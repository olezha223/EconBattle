import { useEffect, useCallback, useRef } from 'react';

export const useWebSocket = (url, onMessage) => {
  const ws = useRef(null);

  // Подключение к WebSocket
  const connect = useCallback(() => {
    ws.current = new WebSocket(url);

    ws.current.onopen = () => {
      console.log('WebSocket connected');
    };

    ws.current.onmessage = (event) => {
      onMessage(JSON.parse(event.data));
    };

    ws.current.onclose = () => {
      console.log('WebSocket disconnected');
      setTimeout(() => connect(), 3000); // Переподключение через 3 сек
    };
  }, [url, onMessage]);

  // Отправка сообщений
  const send = useCallback((data) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(data));
    }
  }, []);

  // Инициализация при монтировании
  useEffect(() => {
    connect();
    return () => {
      if (ws.current?.readyState === WebSocket.OPEN) {
        ws.current.close();
      }
    };
  }, [connect]);

  return { send };
};