import './ProblemForm.module.css'

function ProblemForm({ problem, answer, onAnswerChange }) {
  const handleOptionSelect = (selectedAnswer) => {
    onAnswerChange(selectedAnswer)
  }

  const answerOptions = problem.value?.answers || problem.answers || []
  const questionText = problem.text || problem.question_text || ''

  return (
    <div className="problem-container">
      <h3 className="problem-title">Вопрос за {problem.price} очков</h3>
      <div className="problem-question">{questionText}</div>

      <div className="answer-options">
        {answerOptions.map((option, index) => (
          <button
            key={index}
            className={`option-button ${answer === option ? 'selected' : ''}`}
            onClick={() => handleOptionSelect(option)}
          >
            {String(option)}
          </button>
        ))}
      </div>
    </div>
  )
}

export default ProblemForm