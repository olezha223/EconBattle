import { Routes, Route } from 'react-router-dom';
import Lobby from './components/Lobby';
import Game from './components/Game';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Lobby />} />
      <Route path="/game" element={<Game />} />
    </Routes>
  );
}

export default App;