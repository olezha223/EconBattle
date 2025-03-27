import '../styles/ProblemForm.css'

function ProblemForm({ problem, answer, onAnswerChange }) {
  return (
    <div className="problem-container">
      <h3 className="problem-title">{problem.title}</h3>
      <div className="problem-description">{problem.description}</div>

      <div className="answer-input">
        <label htmlFor="answer">Your answer:</label>
        <input
          id="answer"
          type="text"
          value={answer || ''}
          onChange={(e) => onAnswerChange(e.target.value)}
          placeholder="Enter your answer"
        />
      </div>
    </div>
  )
}

export default ProblemForm