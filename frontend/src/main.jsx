import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { BrowserRouter } from 'react-router-dom';
import { WebsocketProvider } from './contexts/WebsocketContext';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <WebsocketProvider>
        <App />
      </WebsocketProvider>
    </BrowserRouter>
  </React.StrictMode>
);