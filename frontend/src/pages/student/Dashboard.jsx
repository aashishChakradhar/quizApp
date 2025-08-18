import { useState, useEffect } from "react";
import api from "../../api/token.js";
import Chart from "../../components/Chart.jsx";

export default function Dashboard() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
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
      } catch (err) {
        setError("Failed to load records");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchRecords();
  }, []);

  useEffect(() => {
    if (!records.length) return;

    const current_year = new Date().getFullYear();
    const current_month = new Date().getMonth();

    // Filter records for current month
    const filtered = records.filter((record) => {
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
        timestamp: new Date(record.created_at).getTime(),
      });
    });

    // Optional: sort by date for smoother graphs
    Object.keys(grouped).forEach((cat) => {
      grouped[cat].sort((a, b) => a.timestamp - b.timestamp);
    });

    setCategoryData(grouped);
  }, [records]);

  const toggleGraph = () => {
    setGraphType((prev) => (prev === "line" ? "bar" : "line"));
  };

  return (
    <div
      id="display-container"
      style={{ overflow: "scroll", height: "71.5vh" }}
    >
      {loading && <p>Loading records...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
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
            padding: "6px 10px",
            fontSize: "0.8rem",
            cursor: "pointer",
            border: "1px solid #ccc",
            borderRadius: "6px",
            backgroundColor: "#f9f9f9",
          }}
        >
          {graphType === "line" ? "Bar Graph" : "Line Graph"}
        </button>
      </div>

      {!loading && Object.keys(categoryData).length === 0 && (
        <p>No records for this month.</p>
      )}

      {Object.entries(categoryData).map(([category, data], index) => (
        <div key={index} style={{ marginBottom: "1rem" }}>
          <h3>{category}</h3>
          <Chart data={data} type={graphType} />
        </div>
      ))}
    </div>
  );
}
