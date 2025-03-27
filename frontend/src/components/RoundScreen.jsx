import { useState } from 'react'
import ProblemForm from './ProblemForm'
import '../styles/RoundScreen.css'

function RoundScreen({ problems, onSubmit, timeLeft }) {
  const [currentProblemIndex, setCurrentProblemIndex] = useState(0)
  const [answers, setAnswers] = useState(Array(problems.length).fill(null))

  const handleAnswerChange = (index, value) => {
    const newAnswers = [...answers]
    newAnswers[index] = value
    setAnswers(newAnswers)
  }

  const handleNextProblem = () => {
    if (currentProblemIndex < problems.length - 1) {
      setCurrentProblemIndex(currentProblemIndex + 1)
    }
  }

  const handlePrevProblem = () => {
    if (currentProblemIndex > 0) {
      setCurrentProblemIndex(currentProblemIndex - 1)
    }
  }

  const handleSubmit = () => {
    const formattedAnswers = {}
    problems.forEach((_, index) => {
      formattedAnswers[`task${index + 1}`] = answers[index] ? [answers[index]] : []
    })
    onSubmit(formattedAnswers)
  }

  return (
    <div className="round-container">
      <div className="progress-indicator">
        Problem {currentProblemIndex + 1} of {problems.length}
      </div>

      <ProblemForm
        problem={problems[currentProblemIndex]}
        answer={answers[currentProblemIndex]}
        onAnswerChange={(value) => handleAnswerChange(currentProblemIndex, value)}
      />

      <div className="navigation-buttons">
        <button
          onClick={handlePrevProblem}
          disabled={currentProblemIndex === 0}
        >
          Previous
        </button>

        {currentProblemIndex < problems.length - 1 ? (
          <button onClick={handleNextProblem}>Next</button>
        ) : (
          <button onClick={handleSubmit} className="submit-button">
            Submit Answers
          </button>
        )}
      </div>
    </div>
  )
}

export default RoundScreen