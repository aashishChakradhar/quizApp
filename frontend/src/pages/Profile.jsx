import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api/token.js";
export default function Profile(props) {
  //   const { uid } = useParams();
  const [info, setInfo] = useState({
    first_name: "",
    last_name: "",
    email: "",
    username: "",
  });
  const [isEditable, setEditable] = useState(false);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        api.get(`${process.env.REACT_APP_API_URL}/profile/`).then((res) => {
          setInfo(res.data);
        });
      } catch (error) {
        console.error("Error loading your profile:", error);
      }
    };
    fetchProfile();
  }, []);

  const handleChange = (e) => {
    setInfo({
      ...info,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.patch(`${process.env.REACT_APP_API_URL}/update/`, info);
      alert("Detail Updated Successfully");
      setEditable(false);
    } catch (error) {
      alert("Detail Update failed:", error.message);
    }
  };
  const toggleEdit = () => {
    setEditable((prev) => !prev);
  };
  if (!info) return <p>Loading...</p>;
  return (
    <div id="display-container">
      <div id="title">My Account</div>
      <div id="info">
        <form id="details" method="post" onSubmit={handleSubmit}>
          <span
            className="material-symbols-outlined"
            style={{ cursor: "pointer", marginLeft: "auto" }}
            onClick={toggleEdit}
          >
            person_edit
          </span>

          <label htmlFor="first_name">
            <span>First Name:</span>
            <input
              type="text"
              name="first_name"
              value={info.first_name}
              onChange={handleChange}
              disabled={!isEditable}
            />
          </label>
          <label htmlFor="last_name">
            <span>Last Name:</span>
            <input
              type="text"
              name="last_name"
              value={info.last_name}
              onChange={handleChange}
              disabled={!isEditable}
            />
          </label>
          <label htmlFor="email">
            <span>Email:</span>
            <input
              type="text"
              name="email"
              value={info.email}
              onChange={handleChange}
              disabled={!isEditable}
            />
          </label>
          <label htmlFor="username">
            <span>Username:</span>
            <input
              type="text"
              name="username"
              value={info.username}
              onChange={handleChange}
              disabled={!isEditable}
            />
          </label>
          {isEditable && (
            <div id="button-container">
              <button type="submit" hidden={!isEditable}>
                Make Changes
              </button>
            </div>
          )}
        </form>
      </div>
    </div>
  );
}
