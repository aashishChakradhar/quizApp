import { logout } from "../services/authService";
import { useNavigate, Link } from "react-router-dom";

export default function Dashboard() {
  const navigate = useNavigate();
  function handleLogout() {
    logout();
    navigate("/login");
  }
  return (
    <div id="dashboard-container">
      <h2>Welcome to Dashboard</h2>
      dashboar goes here
    </div>
  );
}
