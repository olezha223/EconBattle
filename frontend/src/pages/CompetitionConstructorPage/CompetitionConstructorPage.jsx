import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import MiniPreview from './MiniPreview';
import styles from './CompetitionConstructorPage.module.css';
import {createCompetition, fetchAllTasks, fetchUserTasksPreviews, getUserId} from "../../services/api.js";

const MAX_NAME_LENGTH = 50;
const MAX_ROUNDS = 30;
const MAX_TASKS_PER_ROUND = 50;
const MAX_TIME_LIMIT = 3000;

const TaskSelectorModal = ({ tasks, onClose, onSelect }) => (
  <div className={styles.modalOverlay}>
    <div className={styles.modalContent}>
      <div className={styles.modalHeader}>
        <h3>Выберите задачу</h3>
        <button className={styles.closeButton} onClick={onClose}>×</button>
      </div>
      <div className={styles.previewsContainer}>
        {tasks.map(task => (
          <MiniPreview
            key={task.id}
            task={task}
            onSelect={onSelect}
          />
        ))}
      </div>
    </div>
  </div>
);

export default function CompetitionConstructorPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    tasks_markup: { '1': { tasks: [], time_limit: 60 } }
  });
  const [currentRound, setCurrentRound] = useState('1');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showTaskSelector, setShowTaskSelector] = useState(false);
  const [tasksPreviews, setTasksPreviews] = useState([]);

  const loadTasks = async (source) => {
    try {
      let tasksData;

      if (source === 'my') {
        tasksData = await fetchUserTasksPreviews();
      } else {
        tasksData = await fetchAllTasks();
      }

      setTasksPreviews(tasksData);
    } catch (err) {
      setError(err.message || 'Ошибка загрузки задач');
    }
  };

  const handleTaskSourceSelect = (source) => {
    setShowTaskSelector(true);
    loadTasks(source);
  };

  const handleAddTask = (taskId) => {
    // Проверка максимального количества задач в раунде
    const currentTasksCount = formData.tasks_markup[currentRound].tasks.length;
    if (currentTasksCount >= MAX_TASKS_PER_ROUND) {
      setError(`Нельзя добавить более ${MAX_TASKS_PER_ROUND} задач в один раунд`);
      setShowTaskSelector(false);
      return;
    }

    setFormData(prev => ({
      ...prev,
      tasks_markup: {
        ...prev.tasks_markup,
        [currentRound]: {
          ...prev.tasks_markup[currentRound],
          tasks: [...prev.tasks_markup[currentRound].tasks, taskId]
        }
      }
    }));
    setShowTaskSelector(false);
  };

  const handleAddRound = () => {
    // Проверка максимального количества раундов
    const roundsCount = Object.keys(formData.tasks_markup).length;
    if (roundsCount >= MAX_ROUNDS) {
      setError(`Нельзя создать более ${MAX_ROUNDS} раундов`);
      return;
    }

    const nextRound = String(Number(currentRound) + 1);
    setFormData(prev => ({
      ...prev,
      tasks_markup: {
        ...prev.tasks_markup,
        [nextRound]: { tasks: [], time_limit: 60 }
      }
    }));
    setCurrentRound(nextRound);
  };

  const handleRemoveTask = (round, index) => {
    const updatedTasks = formData.tasks_markup[round].tasks.filter((_, i) => i !== index);
    setFormData(prev => ({
      ...prev,
      tasks_markup: {
        ...prev.tasks_markup,
        [round]: {
          ...prev.tasks_markup[round],
          tasks: updatedTasks
        }
      }
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const competitionData = {
        ...formData,
        creator_id: getUserId(),
        max_rounds: Object.keys(formData.tasks_markup).length,
      };

      await createCompetition(competitionData);
      navigate('/competitions');
    } catch (err) {
      setError(err.response?.data?.detail || 'Ошибка при создании соревнования');
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveRound = (roundToRemove) => {
    if (roundToRemove === '1') return;

    setFormData(prev => {
      const updatedMarkup = { ...prev.tasks_markup };
      delete updatedMarkup[roundToRemove];

      const remainingRounds = Object.keys(updatedMarkup);
      const newCurrentRound = remainingRounds.length > 0
        ? Math.max(...remainingRounds.map(Number)).toString()
        : '1';

      setCurrentRound(newCurrentRound);

      return {
        ...prev,
        tasks_markup: updatedMarkup
      };
    });
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;

    // Ограничение длины названия
    if (name === 'name' && value.length > MAX_NAME_LENGTH) {
      setError(`Название не может превышать ${MAX_NAME_LENGTH} символов`);
      return;
    }

    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleRoundTimeChange = (round, value) => {
    // Проверка максимального времени
    const timeValue = Math.min(Number(value), MAX_TIME_LIMIT);

    setFormData(prev => ({
      ...prev,
      tasks_markup: {
        ...prev.tasks_markup,
        [round]: {
          ...prev.tasks_markup[round],
          time_limit: timeValue
        }
      }
    }));
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Создание нового соревнования</h1>

      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.formGroup}>
          <label className={styles.label}>
            Название соревнования *
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              className={styles.input}
              required
              maxLength={MAX_NAME_LENGTH}
              placeholder={`Максимум ${MAX_NAME_LENGTH} символов`}
            />
          </label>
        </div>

        <div className={styles.formGroup}>
          <label className={styles.label}>
            Разметка задач по раундам
            <div className={styles.roundsContainer}>
              {Object.keys(formData.tasks_markup)
                .sort((a, b) => Number(a) - Number(b))
                .map(round => (
                  <div key={round} className={styles.roundSection}>
                    <div className={styles.roundHeader}>
                      <h3>Раунд {round}</h3>
                      {round !== '1' && (
                        <button
                          type="button"
                          className={styles.removeButton}
                          onClick={() => handleRemoveRound(round)}
                        >
                          ×
                        </button>
                      )}
                    </div>

                    <div className={styles.timeInputContainer}>
                      <label className={styles.label}>
                        Время раунда (сек) *
                        <input
                          type="number"
                          value={formData.tasks_markup[round].time_limit}
                          onChange={(e) => handleRoundTimeChange(round, e.target.value)}
                          className={styles.timeInput}
                          min="10"
                          max={MAX_TIME_LIMIT}
                          required
                        />
                      </label>
                      <p className={styles.hint}>Максимум: {MAX_TIME_LIMIT} секунд</p>
                    </div>

                    <div className={styles.tasksList}>
                      {formData.tasks_markup[round].tasks.map((taskId, index) => (
                        <div key={`${round}-${taskId}`} className={styles.taskItem}>
                          <span>Задача #{taskId}</span>
                          <button
                            type="button"
                            className={styles.removeTaskButton}
                            onClick={() => handleRemoveTask(round, index)}
                          >
                            ×
                          </button>
                        </div>
                      ))}
                    </div>

                    <div className={styles.taskCounter}>
                      Задач: {formData.tasks_markup[round].tasks.length}/{MAX_TASKS_PER_ROUND}
                    </div>

                    <div className={styles.addTaskContainer}>
                      <button
                        type="button"
                        className={styles.sourceButton}
                        onClick={() => {
                          setCurrentRound(round);
                          handleTaskSourceSelect('my');
                        }}
                        disabled={formData.tasks_markup[round].tasks.length >= MAX_TASKS_PER_ROUND}
                      >
                        Добавить из моих задач
                      </button>
                      <button
                        type="button"
                        className={styles.sourceButton}
                        onClick={() => {
                          setCurrentRound(round);
                          handleTaskSourceSelect('all');
                        }}
                        disabled={formData.tasks_markup[round].tasks.length >= MAX_TASKS_PER_ROUND}
                      >
                        Добавить из общего банка
                      </button>
                    </div>
                  </div>
                ))}
            </div>
          </label>

          <div className={styles.roundControls}>
            <button
              type="button"
              className={styles.addRoundButton}
              onClick={handleAddRound}
              disabled={Object.keys(formData.tasks_markup).length >= MAX_ROUNDS}
            >
              Добавить раунд
            </button>
            <div className={styles.roundCounter}>
              Раундов: {Object.keys(formData.tasks_markup).length}/{MAX_ROUNDS}
            </div>
          </div>
        </div>

        {showTaskSelector && (
          <TaskSelectorModal
            tasks={tasksPreviews}
            onClose={() => setShowTaskSelector(false)}
            onSelect={handleAddTask}
          />
        )}

        {error && <div className={styles.error}>{error}</div>}

        <div className={styles.actions}>
          <button
            type="button"
            className={styles.cancelButton}
            onClick={() => navigate(-1)}
            disabled={loading}
          >
            Отменить
          </button>
          <button
            type="submit"
            className={styles.submitButton}
            disabled={loading}
          >
            {loading ? 'Создание...' : 'Создать соревнование'}
          </button>
        </div>
      </form>
    </div>
  );
}