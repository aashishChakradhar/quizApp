import { Navigate } from "react-router-dom";
import { isAuthenticated } from "../services/authService";
import Header from "../components/header";
import Sidebar from "../components/sidebar";

export default function PrivateRoute({ children }) {
  if (!isAuthenticated()) {
    <Navigate to="/login" />;
  }
  return (
    <>
      <Header />
      <div id="body-container">
        <Sidebar />
        {children}
        {/* <Footer /> */}
      </div>
    </>
  );
}

export function TakeExam({ children }) {
  if (!isAuthenticated()) {
    <Navigate to="/login" />;
  }
  return (
    <>
      <div id="body-container">{children}</div>
    </>
  );
}
