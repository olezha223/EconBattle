import { Link, useNavigate } from 'react-router-dom'
import { formatTimeAgo } from '../../utils/timeUtils'
import styles from './TaskPreview.module.css'

export default function TaskPreview({ id, name, creator_name, creator_id, created_at, used_in_competitions }) {
    const navigate = useNavigate()

    const handleContainerClick = () => {
        navigate(`/tasks/${id}`)
    }

    const handleAuthorClick = (e) => {
        e.stopPropagation()
    }

    return (
        <div className={styles.preview} onClick={handleContainerClick}>
            <div className={styles.left}>
                <h3 className={styles.name}>{name}</h3>
                <div className={styles.authorContainer}>
                    <Link
                        to={`/user_page/${creator_id}`}
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
            </div>
            <div className={styles.right}>
                <div className={styles.stat}>
                    <span className={styles.label}>Создано:</span>
                    <span className={styles.value}>{formatTimeAgo(new Date(created_at))}</span>
                </div>
                <div className={styles.stat}>
                    <span className={styles.label}>Использовано:</span>
                    <span className={styles.value}>{used_in_competitions} раз</span>
                </div>
            </div>
        </div>
    )
}