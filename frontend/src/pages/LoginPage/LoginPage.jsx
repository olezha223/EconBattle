import { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import styles from './LoginPage.module.css';

export default function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const originalPath = location.state?.from?.pathname || '/';
    sessionStorage.setItem('preAuthPath', originalPath);

    // Добавляем return_to параметр
    const returnTo = encodeURIComponent(originalPath);
    window.location.href = `http://econ-battle.ru/api/login?return_to=${returnTo}`;
  }, [navigate, location]);

  return <div className={styles.container}>Redirecting to login page...</div>;
}