import { Link, Navigate } from "react-router-dom";
import api from "../api/token.js";
import { useState, useEffect } from "react";
export default function Header(props) {
  const navigate = Navigate;
  const [user, setUser] = useState({ username: "" });
  const greeting =
    new Date().getHours() < 12
      ? "Good Morning"
      : new Date().getHours() < 16
      ? "Good Afternoon"
      : "Good Evening";

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await api.get(`${process.env.REACT_APP_API_URL}/profile/`);
        setUser(res.data);
      } catch (error) {
        navigate("/login");
      }
    };
    fetchUser();
  });
  return (
    <header>
      <Link id="title" to="/dashboard">
        Quizzy Quiz
      </Link>
      <div id="greeting">
        {greeting}, {user.username.toUpperCase()}
      </div>
      <div id="profile">
        <Link to="/profile">
          <span className="material-symbols-outlined">account_circle</span>
        </Link>
      </div>
    </header>
  );
}
