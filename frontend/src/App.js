import "./styles/App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import Dashboard from "./pages/Dashboard";
import Category from "./pages/Category";
import RecordView from "./pages/Records";
import Questions from "./pages/ExamForm";
import Signup from "./pages/Signup";
import PrivateRoute from "./routes/PrivateRoute";
import ChooseExam from "./pages/ExamAlloc";
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/"
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          }
        />
        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          }
        />
        <Route
          path="/test"
          element={
            <PrivateRoute>
              <Questions />
            </PrivateRoute>
          }
        />
        <Route
          path="/records/view"
          element={
            <PrivateRoute>
              <RecordView />
            </PrivateRoute>
          }
        />
        <Route
          path="/category"
          element={
            <PrivateRoute>
              <Category />
            </PrivateRoute>
          }
        />
        <Route
          path="/exams"
          element={
            <PrivateRoute>
              <ChooseExam />
            </PrivateRoute>
          }
        />
        <Route
          path="/exams/:examid/questions"
          element={
            <PrivateRoute>
              <Questions />
            </PrivateRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
