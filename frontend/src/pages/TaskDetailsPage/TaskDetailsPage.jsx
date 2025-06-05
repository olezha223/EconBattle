import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { format } from 'date-fns'
import { ru } from 'date-fns/locale'
import styles from './TaskDetailsPage.module.css'
import {fetchTaskDetails} from "../../services/api.js";


const taskTypes = [
  { value: 'single choice', label: 'Выбрать один вариант' },
  { value: 'multiple choice', label: 'Множественный выбор' },
  { value: 'string', label: 'Вписать строку' },
  { value: 'number', label: 'Вписать число' }
];

const taskTypeLabels = taskTypes.reduce((acc, type) => {
  acc[type.value] = type.label;
  return acc;
}, {});

const formatValue = (value, type) => {
  if (!value?.answers) return 'Нет данных';

  if (Array.isArray(value.answers)) {
    return value.answers.map((item, index) => (
      <li key={index} className={styles.listItem}>
        {JSON.stringify(item)}
      </li>
    ));
  }
  return JSON.stringify(value.answers);
};

const formatCorrectValue = (correctValue) => {
  if (!correctValue?.answers) return 'Нет данных';

  if (Array.isArray(correctValue.answers)) {
    return (
      <ul className={styles.answerList}>
        {correctValue.answers.map((item, index) => (
          <li key={index} className={styles.answerItem}>
            {JSON.stringify(item)}
          </li>
        ))}
      </ul>
    );
  }
  return <div className={styles.singleAnswer}>{JSON.stringify(correctValue.answers)}</div>;
};

export default function TaskDetailsPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [task, setTask] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showAnswer, setShowAnswer] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchTask = async () => {
      try {
        const data = await fetchTaskDetails(id); // Используем вынесенную функцию
        setTask(data);
      } catch (err) {
        setError('Не удалось загрузить задачу');
        console.error('Error fetching task:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchTask();
  }, [id]);

  if (loading) {
    return <div className={styles.loading}>Загрузка задачи...</div>;
  }

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  if (!task) {
    return <div className={styles.error}>Задача не найдена</div>;
  }

  const handleAuthorClick = (e) => {
    e.stopPropagation();
  };

  const showAnswers =
    ['single choice', 'multiple choice'].includes(task.task_type) &&
    task.value?.answers?.length > 0;

  // Получаем русское название типа задачи
  const taskTypeLabel = taskTypeLabels[task.task_type] || task.task_type;

  return (
    <div className={styles.container}>
      <button className={styles.backButton} onClick={() => navigate(-1)}>
        ← Назад
      </button>

      <h1 className={styles.title}>{task.name}</h1>

      <div className={styles.meta}>
        <Link
          to={`/user_page/${task.creator_id}`}
          className={styles.creatorLink}
          onClick={handleAuthorClick}
        >
          <img
            src={task.picture}
            alt="Аватар автора"
            className={styles.creatorAvatar}
          />
          <span className={styles.creator}>Автор: {task.creator_name}</span>
        </Link>
        <span className={styles.date}>
          Создано: {format(new Date(task.created_at), 'dd MMMM yyyy HH:mm', { locale: ru })}
        </span>
      </div>

      <div className={styles.content}>
        <div className={styles.section}>
          <h2 className={styles.sectionTitle}>Условие задачи</h2>
          <p className={styles.text}>{task.text}</p>
        </div>

        <div className={styles.detailsGrid}>
          <div className={styles.detailItem}>
            <span className={styles.detailLabel}>Тип задачи:</span>
            <span className={styles.detailValue}>{taskTypeLabel}</span>
          </div>
          <div className={styles.detailItem}>
            <span className={styles.detailLabel}>Сложность:</span>
            <span className={styles.detailValue}>{task.price} баллов</span>
          </div>
        </div>

        {showAnswers && (
          <div className={styles.section}>
            <h2 className={styles.sectionTitle}>Варианты ответов</h2>
            <ul className={styles.answersList}>{formatValue(task.value, task.task_type)}</ul>
          </div>
        )}

        <div className={styles.answerSection}>
          <button
            className={styles.answerToggle}
            onClick={() => setShowAnswer(!showAnswer)}
          >
            Показать правильный ответ
            <span className={`${styles.arrow} ${showAnswer ? styles.rotated : ''}`}>▼</span>
          </button>

          {showAnswer && (
            <div className={styles.answerContent}>{formatCorrectValue(task.correct_value)}</div>
          )}
        </div>
      </div>
    </div>
  );
}