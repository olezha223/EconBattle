import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getUserId } from '../../services/api'
import axios from 'axios'
import styles from './TaskConstructorPage.module.css'

const API_URL = 'http://localhost:8000'
const taskTypes = [
  { value: 'single choice', label: 'Выбрать один вариант' },
  { value: 'multiple choice', label: 'Множественный выбор' },
  { value: 'string', label: 'Вписать строку' },
  { value: 'number', label: 'Вписать число' }
]
const accessTypes = [
  { value: 'public', label: 'Публичный' },
  { value: 'private', label: 'Приватный' }
]

export default function TaskConstructorPage() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    name: '',
    text: '',
    price: 0,
    task_type: 'single choice',
    value: {},
    correct_value: { input: '' },
    access_type: 'public'
  })
  const [error, setError] = useState('')

  const parseValue = (value, taskType) => {
    try {
      switch(taskType) {
        case 'single choice':
          return [value.trim()]
        case 'multiple choice':
          return JSON.parse(value)
        case 'string':
          return [value.toString()]
        case 'number':
          const numValue = parseFloat(value)
          if (isNaN(numValue)) throw new Error('Некорректное число')
          return [numValue]
        default:
          throw new Error(`Неизвестный тип задачи: ${taskType}`)
      }
    } catch (e) {
      throw new Error(`Ошибка формата: ${e.message}`)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    try {
      const taskType = formData.task_type
      const isChoiceType = ['single choice', 'multiple choice'].includes(taskType)

      // Проверка вариантов ответов для типов с выбором
      const answers = Object.values(formData.value).filter(v => v.trim() !== '')
      if (isChoiceType && answers.length < 2) {
        throw new Error('Добавьте минимум 2 варианта ответа')
      }

      // Проверка правильного ответа
      if (!formData.correct_value.input) {
        throw new Error('Введите правильный ответ')
      }

      // Парсим значение ответа
      const parsedCorrectValue = parseValue(formData.correct_value.input, taskType)

      // Формируем данные для отправки
      const taskData = {
        creator_id: getUserId(),
        name: formData.name,
        text: formData.text,
        price: Number(formData.price),
        task_type: taskType,
        value: isChoiceType ? { answers } : {},
        correct_value: {
          answers: parsedCorrectValue
        },
        access_type: formData.access_type
      }

      await axios.post(`${API_URL}/tasks/`, taskData, { withCredentials: true })
      navigate('/tasks')
    } catch (err) {
      setError(err.response?.data?.detail || err.message)
    }
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleRemoveOption = (keyToRemove) => {
    setFormData(prev => {
      const newValue = { ...prev.value }
      delete newValue[keyToRemove]
      return { ...prev, value: newValue }
    })
  }

  const renderAnswerOptions = () => (
    <div className={styles.section}>
      <h3 className={styles.subtitle}>Варианты ответов</h3>
      <div className={styles.options}>
        {Object.keys(formData.value).map((key, index) => (
          <div key={key} className={styles.optionItem}>
            <input
              type="text"
              value={formData.value[key]}
              onChange={(e) => setFormData(prev => ({
                ...prev,
                value: { ...prev.value, [key]: e.target.value }
              }))}
              className={styles.input}
              placeholder={`Вариант ${index + 1}`}
            />
            <button
              type="button"
              className={styles.removeButton}
              onClick={() => handleRemoveOption(key)}
            >
              ✕
            </button>
          </div>
        ))}
        <button
          type="button"
          className={styles.addButton}
          onClick={() => setFormData(prev => ({
            ...prev,
            value: { ...prev.value, [Date.now()]: '' }
          }))}
        >
          + Добавить вариант
        </button>
      </div>
    </div>
  )

  const renderCorrectAnswerInput = () => {
    const taskType = formData.task_type
    let placeholder = ''
    let hint = null

    if (taskType === 'single choice') {
      placeholder = 'Введите верный вариант ответа'
      hint = 'Введите точную текстовую формулировку правильного варианта'
    } else if (taskType === 'multiple choice') {
      placeholder = 'Введите JSON-массив выбранных вариантов, например: ["Вариант 1", "Вариант 3"]'
      hint = 'Используйте JSON-формат для списка выбранных вариантов'
    } else if (taskType === 'string') {
      placeholder = 'Введите строку'
    } else if (taskType === 'number') {
      placeholder = 'Введите число'
      hint = 'Дробные числа вводите через точку, например: 3.14'
    }

    return (
      <div className={styles.section}>
        <h3 className={styles.subtitle}>Правильный ответ</h3>
        <input
          type="text"
          value={formData.correct_value.input}
          onChange={(e) => setFormData(prev => ({
            ...prev,
            correct_value: { input: e.target.value }
          }))}
          className={styles.input}
          placeholder={placeholder}
        />
        {hint && <p className={styles.hint}>{hint}</p>}
      </div>
    )
  }

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Создание новой задачи</h1>

      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.section}>
          <label className={styles.label}>
            Название задачи *
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

        <div className={styles.section}>
          <label className={styles.label}>
            Условие задачи *
            <textarea
              name="text"
              value={formData.text}
              onChange={handleInputChange}
              className={styles.textarea}
              rows="5"
              required
            />
          </label>
        </div>

        <div className={styles.row}>
          <div className={styles.group}>
            <label className={styles.label}>
              Сложность (баллы) *
              <input
                type="number"
                name="price"
                value={formData.price}
                onChange={handleInputChange}
                className={styles.input}
                min="0"
                required
              />
            </label>
          </div>

          <div className={styles.group}>
            <label className={styles.label}>
              Тип задачи *
              <select
                name="task_type"
                value={formData.task_type}
                onChange={handleInputChange}
                className={styles.select}
              >
                {taskTypes.map(({ value, label }) => (
                  <option key={value} value={value}>
                    {label}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <div className={styles.group}>
            <label className={styles.label}>
              Модификатор доступа *
              <select
                name="access_type"
                value={formData.access_type}
                onChange={handleInputChange}
                className={styles.select}
              >
                {accessTypes.map(({ value, label }) => (
                  <option key={value} value={value}>
                    {label}
                  </option>
                ))}
              </select>
            </label>
            {formData.access_type === 'public' ? (
              <p className={styles.hint}>Все видят вашу задачу и ответ на нее</p>
            ) : (
              <p className={styles.hint}>Только вы можете использовать задачу</p>
            )}
          </div>
        </div>

        {['single choice', 'multiple choice'].includes(formData.task_type) && renderAnswerOptions()}
        {renderCorrectAnswerInput()}

        {error && <div className={styles.error}>{error}</div>}

        <div className={styles.actions}>
          <button
            type="button"
            className={styles.cancel}
            onClick={() => navigate(-1)}
          >
            Отменить
          </button>
          <button type="submit" className={styles.submit}>
            Опубликовать задачу
          </button>
        </div>
      </form>
    </div>
  )
}