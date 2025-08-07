import { useState, useEffect } from "react";
import api from "../api/token.js";
export default function RecordView(porps) {
  const [records, setRecords] = useState([]);
  useEffect(() => {
    api
      .get(`${process.env.REACT_APP_API_URL}/records/view/`)
      .then((res) => setRecords(res.data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div id="display-container">
      Hello records
      <table>
        <thead>
          <tr>
            <th>User</th>
            <th>Category</th>
            <th>Score</th>
            <th>Exam Date</th>
          </tr>
        </thead>
        <tbody>
          {records.map((item, index) => (
            <tr key={index}>
              <td>{item.user}</td>
              <td>{item.category}</td>
              <td>{item.score}</td>
              <td>{item.created_at}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
