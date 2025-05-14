import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './CompetitionConstructorPage.module.css';

const API_URL = 'http://localhost:8000';

export default function CompetitionConstructorPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    max_rounds: 5,
    round_time_in_seconds: 60,
    tasks_markup: {
      '1': [] // Храним ключи раундов как строки
    }
  });
  const [currentRound, setCurrentRound] = useState('1');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [taskInputs, setTaskInputs] = useState({ '1': '' });

  const handleAddRound = () => {
    const nextRound = String(Number(currentRound) + 1);
    setFormData(prev => ({
      ...prev,
      tasks_markup: {
        ...prev.tasks_markup,
        [nextRound]: []
      }
    }));
    setCurrentRound(nextRound);
  };

  const handleAddTask = (round) => {
    const taskId = taskInputs[round];
    if (!taskId || isNaN(taskId)) {
      setError('Введите корректный ID задачи');
      return;
    }

    setFormData(prev => ({
      ...prev,
      tasks_markup: {
        ...prev.tasks_markup,
        [round]: [...(prev.tasks_markup[round] || []), parseInt(taskId)]
      }
    }));
    setTaskInputs(prev => ({ ...prev, [round]: '' }));
    setError('');
  };

  const handleRemoveTask = (round, index) => {
    const updatedTasks = formData.tasks_markup[round].filter((_, i) => i !== index);
    setFormData(prev => ({
      ...prev,
      tasks_markup: {
        ...prev.tasks_markup,
        [round]: updatedTasks
      }
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const competitionData = {
        ...formData,
        creator_id: localStorage.getItem('user_id'),
        max_rounds: Number(formData.max_rounds),
        round_time_in_seconds: Number(formData.round_time_in_seconds)
      };

      await axios.post(`${API_URL}/competitions/`, competitionData, {
        withCredentials: true
      });

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

    // Очищаем связанный ввод
    setTaskInputs(prev => {
      const newInputs = { ...prev };
      delete newInputs[roundToRemove];
      return newInputs;
    });
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
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
            />
          </label>
        </div>

        <div className={styles.grid}>
          <div className={styles.formGroup}>
            <label className={styles.label}>
              Макс. раундов *
              <input
                type="number"
                name="max_rounds"
                value={formData.max_rounds}
                onChange={handleInputChange}
                className={styles.input}
                min="1"
                max="20"
                required
              />
            </label>
          </div>

          <div className={styles.formGroup}>
            <label className={styles.label}>
              Время раунда (сек) *
              <input
                type="number"
                name="round_time_in_seconds"
                value={formData.round_time_in_seconds}
                onChange={handleInputChange}
                className={styles.input}
                min="10"
                max="3600"
                required
              />
            </label>
          </div>
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

                    <div className={styles.tasksList}>
                      {formData.tasks_markup[round].map((taskId, index) => (
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

                    <div className={styles.addTaskContainer}>
                      <input
                        type="number"
                        value={taskInputs[round] || ''}
                        onChange={(e) => setTaskInputs(prev => ({
                          ...prev,
                          [round]: e.target.value
                        }))}
                        placeholder="Введите ID задачи"
                        className={styles.taskInput}
                      />
                      <button
                        type="button"
                        className={styles.addTaskButton}
                        onClick={() => handleAddTask(round)}
                      >
                        Добавить задачу
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
            >
              Добавить раунд
            </button>
          </div>
        </div>

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