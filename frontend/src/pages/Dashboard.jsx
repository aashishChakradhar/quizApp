
import React from 'react';
import { logout } from '../services/authService';

export default function Dashboard() {
  return (
    <div>
      <h2>Welcome to Dashboard</h2>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
