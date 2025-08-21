import { useState, useEffect } from "react";
import api from "../../api/token.js";

export default function CreateExam() {
  const [examTitle, setExamTitle] = useState("");
  const [categories, setCategory] = useState([]);
  const [groups, setGroups] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("");
  const [selectedGroup, setSelectedGroup] = useState([]);
  const [point, setPoint] = useState(0);
  const [date, setDate] = useState(new Date());

  useEffect(() => {
    api
      .get(`${process.env.REACT_APP_API_URL}/teacher/create-exam/`)
      .then((res) => {
        setCategory(res.data.categories);
        setGroups(res.data.groups);
      })
      .catch((error) => alert(error));
  }, []);

  const handleExamTitle = (e) => setExamTitle(e.target.value);
  const handleCategory = (e) => setSelectedCategory(e.target.value);
  const handleGroup = (e) => setGroups(e.target.value);
  const handlePoint = (e) => setPoint(e.target.value);
  const handleDate = (e) => setDate(new Date(e.target.value));

  const handleSubmit = (e) => {
    e.preventDefault();
    const data = {
      title: examTitle,
      category: selectedCategory,
      groups: selectedGroup,
      total_points: Number(point),
      deadline: date.toISOString().split("T")[0],
    };
    api
      .post(`${process.env.REACT_APP_API_URL}/teacher/create-exam/`, data)
      .then(
        setPoint(0),
        setSelectedCategory(""),
        setSelectedGroup([]),
        setExamTitle("")
      )
      .catch((error) => alert("Unable to create exam:here", error));
  };
  return (
    <div id="display-container">
      <div className="center-block">
        <form action="" id="details" method="post" onSubmit={handleSubmit}>
          <label htmlFor="exam-title">
            <span>Exam Title</span>
            <input
              type="text"
              id="exam-title"
              placeholder="Exam Title"
              value={examTitle}
              onChange={handleExamTitle}
              required
            />
          </label>

          <label htmlFor="category">
            <span>Exam Topic</span>
            <select
              id="category"
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              required
            >
              <option value="">--- Select Topic ---</option>
              {categories.map((category) => (
                <option key={category.uid} value={category.uid}>
                  {category.category_name}
                </option>
              ))}
            </select>
          </label>

          <label>
            <span>Exam Groups</span>
            <div>
              {groups.map((group) => (
                <label key={group.uid} style={{ display: "block" }}>
                  <input
                    type="checkbox"
                    value={group.uid}
                    checked={selectedGroup.includes(group.uid)}
                    onChange={(e) => {
                      const value = e.target.value;
                      if (e.target.checked) {
                        setSelectedGroup([...selectedGroup, value]);
                      } else {
                        setSelectedGroup(
                          selectedGroup.filter((id) => id !== value)
                        );
                      }
                    }}
                  />
                  {group.name}
                </label>
              ))}
            </div>
          </label>

          <label htmlFor="score">
            <span>Total Score</span>
            <input
              type="number"
              id="score"
              placeholder="Total Score"
              value={point}
              onChange={handlePoint}
              required
            />
          </label>
          <label htmlFor="date">
            <span>Date</span>
            <input
              type="date"
              name="date"
              id="date"
              value={date.toISOString().split("T")[0]} // convert to YYYY-MM-DD
              onChange={handleDate}
              required
            />
          </label>

          <div id="button-container">
            <button id="submit-btn">Create Exam</button>
          </div>
        </form>
      </div>
    </div>
  );
}
