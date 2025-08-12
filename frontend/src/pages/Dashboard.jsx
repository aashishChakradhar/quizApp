import { logout } from "../services/authService";
import { useState, useEffect } from "react";
import api from "../api/token.js";
import BarGraph from "../components/bargraph";
import { useNavigate, Link } from "react-router-dom";

export default function Dashboard() {
  const [records, setRecords] = useState([]);
  const [activeRecords, setActiveRecords] = useState([]);
  useEffect(() => {
    api
      .get(`${process.env.REACT_APP_API_URL}/records/view/`)
      .then((res) => {
        setRecords(res.data);
        const current_year = new Date().getFullYear();
        const current_month = new Date().getMonth();
        const filtered = res.data.filter((record) => {
          const recordDate = new Date(record.created_at);
          return (
            recordDate.getMonth() === current_month &&
            recordDate.getFullYear() === current_year
          );
        });
        // Transform records to add a "name" field for the chart X-axis
        const transformed = filtered.map((record) => ({
          name: `${record.category}`, // customize label
          score: record.score,
          uid: record.uid,
        }));

        setActiveRecords(transformed);
      })
      .catch((err) => console.error(err));
  }, []);

  return (
    <div id="display-container">
      Track your Records
      <BarGraph data={activeRecords} />
    </div>
  );
}
