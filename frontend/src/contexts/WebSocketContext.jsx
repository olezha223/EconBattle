// contexts/WebSocketContext.jsx
import { createContext, useContext, useRef } from 'react';

const WebSocketContext = createContext(null);

export const WebSocketProvider = ({ children }) => {
  const ws = useRef(null);

  const sendMessage = (message) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message));
    } else {
      console.error("WebSocket is not connected");
    }
  };

  const connect = (url) => {
    ws.current = new WebSocket(url);

    ws.current.onopen = () => {
      console.log("WebSocket connected");
    };

    ws.current.onclose = () => {
      console.log("WebSocket disconnected");
    };
  };

  return (
    <WebSocketContext.Provider value={{ sendMessage, connect }}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocketContext = () => useContext(WebSocketContext);