import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import api from "../api/token.js";

export default function Questions(props) {
  const { examid } = useParams();
  const [questions, setQuestions] = useState([]);
  const [selectedAnswer, setSelectedAnswer] = useState({});
  useEffect(() => {
    if (examid) {
      api
        .get(`${process.env.REACT_APP_API_URL}/exams/${examid}/questions/`)
        .then((res) => setQuestions(res.data))
        .catch((err) => console.error("Error Loading Questions:", err));
    }
    api
      .get(`${process.env.REACT_APP_API_URL}/questions/`)
      .then((res) => setQuestions(res.data))
      .catch((err) => console.error(err));
  }, []);

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
    } catch (err) {
      console.error("Submission failed:", err);
      alert("Submission failed");
    }
  };

  return (
    <div id="display-container">
      <form method="post" onSubmit={handleSubmission}>
        <h1>Test</h1>
        <div>
          {questions.map((question, index) => (
            <div key={question.uid} className="question-block">
              <h3>
                {index + 1}. {question.question}
              </h3>
              {question.question_answer.map((answer, index) => (
                <label key={answer.uid}>
                  <input
                    type="radio"
                    name={`question-${question.uid}`}
                    value={answer.uid}
                    checked={selectedAnswer[question.uid] === answer.uid}
                    onChange={() => handleSelection(question.uid, answer.uid)}
                  />
                  {answer.answer}
                </label>
              ))}
            </div>
          ))}
        </div>
        <button id="submit-btn" type="submit">
          Submit
        </button>
      </form>
    </div>
  );
}
