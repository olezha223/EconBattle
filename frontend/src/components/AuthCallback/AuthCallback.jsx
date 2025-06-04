import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';

export default function AuthCallbackPage() {
  const navigate = useNavigate();

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const userToken = params.get('user');
    const returnTo = params.get('return_to') || '/';

    if (!userToken) {
      navigate('/login', { state: { error: "Отсутствуют данные пользователя" } });
      return;
    }

    try {
      // Декодируем JWT без проверки подписи (только для фронтенда)
      const decoded = jwtDecode(userToken);

      // Проверяем срок действия
      const now = Date.now() / 1000;
      if (decoded.exp < now) {
        throw new Error("Токен просрочен");
      }

      localStorage.setItem('user_id', decoded.sub);
      localStorage.setItem('username', decoded.name);
      if (decoded.picture) {
        localStorage.setItem('picture', decoded.picture);
      }

      // Перенаправляем на исходную страницу
      navigate(returnTo);
    } catch (error) {
      console.error('Ошибка обработки авторизации:', error);
      navigate('/login', { state: { error: "Ошибка авторизации" } });
    }
  }, [navigate]);

  return <div>Завершение авторизации...</div>;
}