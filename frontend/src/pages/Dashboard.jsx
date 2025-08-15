import { useState, useEffect } from "react";
import api from "../api/token.js";
import LineGraph from "../components/linegraph";
import BarGraph from "../components/bargraph";

export default function Dashboard() {
  const [records, setRecords] = useState([]);
  const [categoryData, setCategoryData] = useState({});
  const [graphType, setGraphType] = useState("line"); // default to line graph

  useEffect(() => {
    const fetchRecords = async () => {
      try {
        const res = await api.get(
          `${process.env.REACT_APP_API_URL}/records/view/`
        );
        setRecords(res.data);

        const current_year = new Date().getFullYear();
        const current_month = new Date().getMonth();

        // Filter records for current month
        const filtered = res.data.filter((record) => {
          const recordDate = new Date(record.created_at);
          return (
            recordDate.getMonth() === current_month &&
            recordDate.getFullYear() === current_year
          );
        });

        // Group records by category
        const grouped = {};
        filtered.forEach((record) => {
          if (!grouped[record.category]) grouped[record.category] = [];
          grouped[record.category].push({
            name: new Date(record.created_at).toLocaleDateString(),
            score: record.score,
          });
        });

        // Optional: sort by date for smoother graphs
        Object.keys(grouped).forEach((cat) => {
          grouped[cat].sort((a, b) => new Date(a.name) - new Date(b.name));
        });

        setCategoryData(grouped);
      } catch (err) {
        console.error(err);
      }
    };

    fetchRecords();
  }, []);

  const toggleGraph = () => {
    setGraphType((prev) => (prev === "line" ? "bar" : "line"));
  };

  return (
    <div
      id="display-container"
      style={{ overflow: "scroll", height: "71.5vh" }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <span style={{ fontSize: "1.5rem", fontWeight: "700" }}>
          Track your record
        </span>
        <button
          onClick={toggleGraph}
          style={{
            margin: "0",
            padding: "4px",
            fontSize: "0.8rem",
            cursor: "pointer",
            backgroundColor: "transparent",
          }}
        >
          {graphType === "line" ? "Bar Graph" : "Line Graph"}
        </button>
      </div>

      {Object.keys(categoryData).length === 0 && (
        <p>No records for this month.</p>
      )}

      {Object.entries(categoryData).map(([category, data], index) => (
        <div key={index} style={{ marginBottom: "1rem" }}>
          <h3>{category}</h3>
          {graphType === "line" ? (
            <LineGraph data={data} />
          ) : (
            <BarGraph data={data} />
          )}
        </div>
      ))}
    </div>
  );
}
