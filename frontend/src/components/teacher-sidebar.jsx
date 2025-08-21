import { logout } from "../services/authService";
import { useNavigate, Link } from "react-router-dom";
export default function TeacherSidebar(props) {
  const navigate = useNavigate();
  function handleLogout() {
    logout();
    navigate("/login");
  }
  return (
    <div id="sidebar">
      <ul>
        <li>
          <Link to="/teacher/dashboard">Dashboard</Link>
        </li>
        <li>
          <Link to="/teacher/create-group">Create Group</Link>
        </li>
        {/* <li>
          <Link to="/category">View Category</Link>
        </li> */}
        <li>
          <Link to="/teacher/create-exam">Create Exam</Link>
        </li>
      </ul>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
}
