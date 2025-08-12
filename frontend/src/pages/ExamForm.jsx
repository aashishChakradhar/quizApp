import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api/token.js";

export default function Questions(props) {
  const { examid } = useParams();
  const [questions, setQuestions] = useState([]);
  const [selectedAnswer, setSelectedAnswer] = useState({});
  const [currentIndex, setCurrentIndex] = useState(0); // Track which question to show

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        let res;
        if (examid) {
          res = await api.get(
            `${process.env.REACT_APP_API_URL}/exams/${examid}/questions/`
          );
        } else {
          res = await api.get(`${process.env.REACT_APP_API_URL}/questions/`);
        }
        setQuestions(res.data);
      } catch (err) {
        console.error("Error loading questions:", err);
      }
    };
    fetchQuestions();
  }, [examid]);

  const handleSelection = (questionId, answerId) => {
    setSelectedAnswer((prev) => ({
      ...prev,
      [questionId]: answerId,
    }));
  };

  const handleSubmission = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        answers: Object.entries(selectedAnswer).map(
          ([question, selected_answer]) => ({
            question,
            selected_answer,
          })
        ),
      };

      const res = await api.post(
        `${process.env.REACT_APP_API_URL}/questions/submit-test/`,
        payload
      );

      console.log("Submitted successfully:", res.data);
      alert("Test submitted successfully!");
      setSelectedAnswer({});
      setCurrentIndex(0);
    } catch (err) {
      console.error("Submission failed:", err);
      alert("Submission failed");
    }
  };

  const goToQuestion = (index) => {
    if (index >= 0 && index < questions.length) {
      setCurrentIndex(index);
    }
  };

  const navigate = useNavigate();
  const handleExit = () => {
    const shouldExit = window.confirm(
      "Are you sure you want to exit? Your progress will be lost and exam will be invlid."
    );
    if (shouldExit) {
      navigate("/exams");
    }
  };

  if (questions.length === 0) {
    return <p>Loading questions...</p>;
  }

  const currentQuestion = questions[currentIndex];

  return (
    <div id="display-container-question">
      {/* Sidebar for question numbers */}
      <div id="sidebar-question">
        <div id="question-index">
          {questions.map((_, index) => (
            <button
              key={index}
              style={{
                color:
                  index === currentIndex || selectedAnswer[questions[index].uid]
                    ? "white"
                    : "black",
                backgroundColor:
                  index === currentIndex
                    ? "blue"
                    : selectedAnswer[questions[index].uid]
                    ? "lightgreen"
                    : "white",
              }}
              onClick={() => goToQuestion(index)}
            >
              {index + 1}
            </button>
          ))}
        </div>
        <button id="exit-button" onClick={handleExit}>
          {" "}
          Exit Exam
        </button>
      </div>

      {/* Main question area */}
      <form method="post" id="question-form" style={{ flex: 1 }}>
        <h1>
          Question {currentIndex + 1} of {questions.length}
        </h1>
        <div key={currentQuestion.uid} className="question-block">
          <h3>{currentQuestion.question}</h3>
          {currentQuestion.question_answer.map((answer) => (
            <label key={answer.uid} style={{ display: "block" }}>
              <input
                type="radio"
                name={`question-${currentQuestion.uid}`}
                value={answer.uid}
                checked={selectedAnswer[currentQuestion.uid] === answer.uid}
                onChange={() =>
                  handleSelection(currentQuestion.uid, answer.uid)
                }
              />
              {answer.answer}
            </label>
          ))}
        </div>

        {/* Navigation buttons */}
        <div style={{ marginTop: "20px" }}>
          <button
            type="button"
            disabled={currentIndex === 0}
            onClick={() => goToQuestion(currentIndex - 1)}
          >
            Back
          </button>

          {currentIndex < questions.length - 1 ? (
            <button
              type="button"
              onClick={() => goToQuestion(currentIndex + 1)}
              style={{ marginLeft: "10px" }}
            >
              Next
            </button>
          ) : (
            <button
              type="button"
              style={{ marginLeft: "10px", backgroundColor: "green" }}
              onClick={handleSubmission}
            >
              Submit
            </button>
          )}
        </div>
      </form>
    </div>
  );
}
