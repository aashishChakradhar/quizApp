import { useState, useEffect } from "react";
import api from "../api/token.js";
export default function RecordView(porps) {
  const [records, setRecords] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState([]);
  useEffect(() => {
    api
      .get(`${process.env.REACT_APP_API_URL}/records/view/`)
      .then((res) => {
        setRecords(res.data);
        setFiltered(res.data);
        const uniqueCategories = Array.from(
          new Set(res.data.map((record) => record.category))
        );
        setCategories(uniqueCategories);
      })
      .catch((err) => console.error(err));
  }, []);
  function handleFilter(e) {
    const category = e.target.value;
    setSelectedCategory(category);

    if (category === "") {
      setFiltered(records);
    } else {
      const filtered = records.filter((record) => record.category === category);
      setFiltered(filtered);
    }
  }
  return (
    <div id="display-container">
      <div id="filter">
        Topics:
        <select
          style={{ marginRight: "auto" }}
          name="category"
          id="category"
          value={selectedCategory}
          onChange={handleFilter}
        >
          <option value="">-- Topics --</option>
          {categories.map((category, index) => (
            <option key={index} value={category}>
              {category}
            </option>
          ))}
        </select>
      </div>
      <table>
        <thead>
          <tr>
            <th>Category</th>
            <th>Score</th>
            <th>Exam Date</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map((item, index) => (
            <tr key={index}>
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
