import React from 'react';
import { useNavigate } from 'react-router-dom';
import './LoginErrorPage.module.css';

const LoginErrorPage = () => {
  const navigate = useNavigate();

  // Обработчик повторной попытки входа (возвращает на главную)
  const handleRetryLogin = () => {
    navigate('/');
  };

  return (
    <div className="login-error-container">
      <div className="error-card">
        <h1 className="error-title">Что-то пошло не так во время аутентификации...</h1>

        <button
          className="retry-button"
          onClick={handleRetryLogin}
        >
          Попробовать войти еще раз
        </button>

        <p className="support-text">
          Если вы уверены, что ошибка на нашей стороне,
          опишите проблему на почту
          <a href="mailto:oashvetsov@edu.hse.ru" className="email-link">
            oashvetsov@edu.hse.ru
          </a>
        </p>
      </div>
    </div>
  );
};

export default LoginErrorPage;