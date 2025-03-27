// components/ProblemForm.jsx
import '../styles/ProblemForm.css'

function ProblemForm({ problem, answer, onAnswerChange }) {
  const handleOptionSelect = (selectedAnswer) => {
    onAnswerChange(selectedAnswer)
  }

  return (
    <div className="problem-container">
      <h3 className="problem-title">Вопрос за {problem.price} очков</h3>
      <div className="problem-question">{problem.question_text}</div>

      <div className="answer-options">
        {problem.answers.options.map((option, index) => (
          <button
            key={index}
            className={`option-button ${answer === option ? 'selected' : ''}`}
            onClick={() => handleOptionSelect(option)}
          >
            {option}
          </button>
        ))}
      </div>
    </div>
  )
}

export default ProblemForm