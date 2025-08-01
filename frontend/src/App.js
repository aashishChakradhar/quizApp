import './styles/App.css';

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import Category from './pages/Category';
import Test from './pages/Exam';
import PrivateRoute from './routes/PrivateRoute';
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          }
        />
        <Route path='/test' element={< Test />} />
        <Route path='/category' element={<Category />} />
      </Routes>
    </Router>
  );
}

export default App;
