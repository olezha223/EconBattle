import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import styles from './Header.module.css';
import {fetchPictureUrl} from "../../services/api.js";


// Заголовок страницы
export default function Header() {
  const [pictureUrl, setPictureUrl] = useState('');

  // загрузка данных
  useEffect(() => {
    const loadPicture = async () => {
      const url = await fetchPictureUrl();
      setPictureUrl(url);
    };
    loadPicture();
  }, []);

  return (
    <header className={styles.header}>
      <div className={styles.logo}>
        <Link to="/competitions">Экономические бои</Link>
      </div>

      <nav className={styles.nav}>
        <Link to="/profile" className={styles.profileLink}>
          <img
            src={pictureUrl}
            alt="Profile"
            className={styles.avatar}
          />
        </Link>
      </nav>
    </header>
  )
}