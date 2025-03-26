function WaitingForOpponent({ opponentId }) {
  return (
    <div className="waiting-screen">
      {opponentId ? (
        <div className="matched-message">
          Ваш соперник: <span className="opponent-id">{opponentId}</span>
        </div>
      ) : (
        <div className="waiting-message">Ожидаем соперника...</div>
      )}
    </div>
  );
}

export default WaitingForOpponent;