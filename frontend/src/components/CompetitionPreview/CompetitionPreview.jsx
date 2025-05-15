import { useNavigate, Link } from 'react-router-dom'
import { formatTimeAgo } from '../../utils/timeUtils'
import styles from './CompetitionPreview.module.css'
import {getUserId} from "../../services/api.js";

export default function CompetitionPreview({
  id,
  name,
  games_played,
  unique_players,
  created_at,
  creator_id,
  creator_name
}) {
  const navigate = useNavigate()

  const handleContainerClick = () => {
    navigate(`/competitions/${id}`)
  }

  const handleStartButtonClick = (e) => {
    e.stopPropagation();
    navigate(`/game/${id}`);
  };

  const handleAuthorClick = (e) => {
    e.stopPropagation()
  }

  // Определяем путь для профиля автора
  const getAuthorProfilePath = () => {
    return creator_id.toString() === getUserId()
      ? '/profile' // Путь к своему профилю
      : `/user_page/${creator_id}` // Путь к чужому профилю
  }

  return (
    <div className={styles.preview} onClick={handleContainerClick}>
      <div className={styles.content}>
        <h3 className={styles.name}>{name}</h3>
        <div className={styles.authorContainer}>
          <Link
            to={getAuthorProfilePath()}
            className={styles.creatorLink}
            onClick={handleAuthorClick}
          >
            <img
              src="/static/default-avatar.jpg"
              alt="Аватар автора"
              className={styles.creatorAvatar}
            />
            <span className={styles.creator}>{creator_name}</span>
          </Link>
        </div>
        <div className={styles.stats}>
          <span>Игр сыграно: {games_played}</span>
          <span>Уникальных игроков: {unique_players}</span>
        </div>
        <button className={styles.button} onClick={handleStartButtonClick}>
          Начать!
        </button>
      </div>
      <div className={styles.time}>
        {formatTimeAgo(new Date(created_at))}
      </div>
    </div>
  )
}