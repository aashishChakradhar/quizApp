import { useState, useEffect } from "react";
import api from "../../api/token.js";

export default function CreateGroup() {
  const [students, setStudents] = useState([]);
  const [grouped, setGrouped] = useState([]);
  const [groupName, setGroupName] = useState("");

  useEffect(() => {
    api
      .get(`${process.env.REACT_APP_API_URL}/teacher/create-group/`)
      .then((res) => {
        setStudents(res.data);
      })
      .catch((error) => alert(error));
  }, []);

  const handleSubmission = (e) => {
    e.preventDefault();
    const data = {
      name: groupName,
      students: grouped,
    };
    console.log({ name: groupName, students: grouped });
    api
      .post(`${process.env.REACT_APP_API_URL}/teacher/create-group/`, data)
      .then((res) => {
        setGroupName("");
        setGrouped([]);
      })
      .catch((error) => {
        alert("Error Creating Group", error);
      });
  };

  const handleGroupName = (e) => {
    setGroupName(e.target.value);
  };

  const handleSelect = (e) => {
    const value = parseInt(e.target.value);
    setGrouped((prev) =>
      prev.includes(value)
        ? prev.filter((id) => id !== value)
        : [...prev, value]
    );
  };
  return (
    <div id="display-container">
      <form action="" method="post" onSubmit={handleSubmission}>
        <div id="title">Create Group</div>
        <input
          type="text"
          placeholder="Group Name"
          value={groupName}
          onChange={handleGroupName}
          required
        />
        {students.map((student) => (
          <div key={student.uid}>
            <input
              type="checkbox"
              checked={grouped.includes(student.uid)}
              value={student.uid}
              onChange={handleSelect}
            />
            <label htmlFor={student.uid}>
              {student.first_name}_{student.last_name}
            </label>
          </div>
        ))}
        <button>Create Group</button>
      </form>
    </div>
  );
}
