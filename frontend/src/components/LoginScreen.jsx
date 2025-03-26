import { useState } from 'react';

function LoginScreen({ onLogin }) {
  const [inputId, setInputId] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputId.trim()) {
      onLogin(inputId.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="login-form">
      <input
        type="text"
        value={inputId}
        onChange={(e) => setInputId(e.target.value)}
        placeholder="Введите имя"
        className="login-input"
      />
      <button type="submit" className="login-button">
        Найти соперника
      </button>
    </form>
  );
}

export default LoginScreen;