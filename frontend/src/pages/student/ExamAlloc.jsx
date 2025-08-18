import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../../api/token";

export default function ChooseExam(props) {
  const [exams, setExams] = useState([]);

  //   fetch exam
  useEffect(() => {
    api
      .get(`${process.env.REACT_APP_API_URL}/exams/`)
      .then((res) => setExams(res.data))
      .catch((err) => console.error(err));
  }, []);
  return (
    <div id="display-container">
      <h2>Available exam</h2>
      <ul style={{ listStyleType: "none" }}>
        {exams.map((exam, index) => (
          <li key={index}>
            <Link
              to={`/exams/${exam.uid}/questions`}
              style={{
                fontSize: "1.2rem",
                fontWeight: "700",
                textDecoration: "none",
              }}
            >
              {exam.category}: {exam.title}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
