import React from 'react';
import { logout } from '../services/authService';
import {useNavigate,Link} from 'react-router-dom';
 

export default function Dashboard() {
  const navigate = useNavigate();
  function handleLogout(){
    logout();
    navigate('/login')
  }
  return (
    <div id='dashboard-container'>
      <h2>Welcome to Dashboard</h2>
      <ul>
        <li><Link to="/test">Take exam</Link></li>
        <li><Link to="/category">View Report</Link></li>
        <li><Link to="/category">View Exam</Link></li>
      </ul>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
}
