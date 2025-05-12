import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getUserId } from '../../services/api'
import axios from 'axios'
import styles from './TaskConstructorPage.module.css'

const API_URL = 'http://localhost:8000'
const taskTypes = ['single choice', 'multiple choice', 'text', 'number']
const answerTypes = ['string', 'float', 'int', 'list[int]', 'list[str]', 'list[float]']

export default function TaskConstructorPage() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    name: '',
    text: '',
    price: 0,
    task_type: 'single choice',
    value: {},
    answer_type: 'string',
    correct_value: { input: '' }
  })
  const [error, setError] = useState('')

  const parseValue = (value, type) => {
    try {
      switch(type) {
        case 'int': return parseInt(value)
        case 'float': return parseFloat(value)
        case 'list[int]': return JSON.parse(value).map(Number)
        case 'list[str]': return JSON.parse(value)
        case 'list[float]': return JSON.parse(value).map(parseFloat)
        default: return value.toString()
      }
    } catch (e) {
      throw new Error(`Некорректный формат для типа ${type}`)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    try {
      const answers = Object.values(formData.value)
        .filter(v => v.trim() !== '')
        .map(v => v.trim())

      if (['single choice', 'multiple choice'].includes(formData.task_type) && answers.length < 2) {
        throw new Error('Добавьте минимум 2 варианта ответа')
      }

      if (!formData.correct_value.input) {
        throw new Error('Введите правильный ответ')
      }

      const parsedCorrectValue = parseValue(
        formData.correct_value.input,
        formData.answer_type
      )

      const taskData = {
        creator_id: getUserId(),
        name: formData.name,
        text: formData.text,
        price: Number(formData.price),
        task_type: formData.task_type.replace(' ', '_'),
        value: { answers },
        answer_type: formData.answer_type,
        correct_value: {
          answers: Array.isArray(parsedCorrectValue)
            ? parsedCorrectValue
            : [parsedCorrectValue]
        }
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
    const isListType = formData.answer_type.startsWith('list')
    const placeholder = isListType
      ? 'Введите в формате JSON, например: [1, "два", 3]'
      : 'Введите значение'

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
        {isListType && (
          <p className={styles.hint}>
            Используйте JSON-формат для списка значений
          </p>
        )}
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
                {taskTypes.map(type => (
                  <option key={type} value={type}>
                    {type.charAt(0).toUpperCase() + type.slice(1)}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <div className={styles.group}>
            <label className={styles.label}>
              Тип ответа *
              <select
                name="answer_type"
                value={formData.answer_type}
                onChange={handleInputChange}
                className={styles.select}
              >
                {answerTypes.map(type => (
                  <option key={type} value={type}>
                    {type.replace('list', 'Список ')}
                  </option>
                ))}
              </select>
            </label>
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