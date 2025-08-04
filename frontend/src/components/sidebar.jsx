import { logout } from "../services/authService";
import { useNavigate, Link } from "react-router-dom";
export default function Sidebar(props) {
  const navigate = useNavigate();
  function handleLogout() {
    logout();
    navigate("/login");
  }
  return (
    <sidebar>
      <ul>
        <li>
          <Link to="/test">Take exam</Link>
        </li>
        <li>
          <Link to="/records/view">View Report</Link>
        </li>
        <li>
          <Link to="/category">View Exam</Link>
        </li>
      </ul>
      <button onClick={handleLogout}>Logout</button>
    </sidebar>
  );
}
