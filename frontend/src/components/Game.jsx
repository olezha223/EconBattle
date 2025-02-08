import { useEffect, useState } from 'react';
import { useWebSocketContext } from '../contexts/WebSocketContext';
import Timer from './Timer';

export default function Game() {
  const { sendMessage, lastMessage } = useWebSocketContext();
  const [problems, setProblems] = useState([]);
  const [timeLeft, setTimeLeft] = useState(180);

  useEffect(() => {
    if (lastMessage?.data) {
      const data = JSON.parse(lastMessage.data);
      switch (data.type) {
        case 'round_start':
          setProblems(data.problems);
          setTimeLeft(180);
          break;
        case 'timer_update':
          setTimeLeft(data.timeLeft);
          break;
      }
    }
  }, [lastMessage]);

  const handleAnswerSubmit = (problemId, answer) => {
    sendMessage(JSON.stringify({
      type: 'submit_answer',
      problemId,
      answer: parseInt(answer)
    }));
  };

  return (
    <div>
      <h2>Раунд начался!</h2>
      <Timer timeLeft={timeLeft} />
      {problems.map((problem) => (
        <div key={problem.id}>
          <h3>{problem.question}</h3>
          <input
            type="number"
            onChange={(e) => handleAnswerSubmit(problem.id, e.target.value)}
          />
        </div>
      ))}
    </div>
  );
}