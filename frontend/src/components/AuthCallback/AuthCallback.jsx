import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';
import {getUserId} from "../../services/api.js";

export default function AuthCallbackPage() {
  const navigate = useNavigate();

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const userToken = params.get('user');
    const returnTo = params.get('return_to') || '/competitions';

    if (!userToken) {
      navigate('/login', { state: { error: "Отсутствуют данные пользователя" } });
      return;
    }

    try {
      const decoded = jwtDecode(userToken);

      const now = Date.now() / 1000;
      if (decoded.exp < now) {
        throw new Error("Токен просрочен");
      }

      localStorage.setItem('user_id', decoded.sub);
      localStorage.setItem('username', decoded.name);
      if (decoded.picture) {
        localStorage.setItem('picture', decoded.picture);
      }
      console.log(getUserId())
      window.dispatchEvent(new Event('storage'));
      setTimeout(() => {
        navigate(returnTo);
      }, 100);
      console.log(getUserId())
    } catch (error) {
      console.error('Ошибка обработки авторизации:', error);
      navigate('/login', { state: { error: "Ошибка авторизации" } });
    }
  }, [navigate]);

  return <div>Завершение авторизации...</div>;
}