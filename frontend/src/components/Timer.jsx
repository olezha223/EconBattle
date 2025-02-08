import { useEffect } from 'react';

export default function Timer({ timeLeft }) {
  useEffect(() => {
    const timer = document.getElementById('timer');
    timer.style.setProperty('--progress', `${(timeLeft / 180) * 100}%`);
  }, [timeLeft]);

  return (
    <div className="timer-container">
      <div className="timer-progress" id="timer">
        {timeLeft} сек
      </div>
    </div>
  );
}