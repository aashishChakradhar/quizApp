import { logout } from "../services/authService";
import { useNavigate, Link } from "react-router-dom";
export default function Sidebar(props) {
  const navigate = useNavigate();
  function handleLogout() {
    logout();
    navigate("/login");
  }
  return (
    <div id="sidebar">
      <ul>
        <li>
          <Link to="/dashboard">Dashboard</Link>
        </li>
        <li>
          <Link to="/records/view">View Report</Link>
        </li>
        {/* <li>
          <Link to="/category">View Category</Link>
        </li> */}
        <li>
          <Link to="/exams">View Exam</Link>
        </li>
      </ul>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
}
