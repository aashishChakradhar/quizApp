import { Navigate } from "react-router-dom";
import { isAuthenticated } from "../services/authService";
import Header from "../components/header";
import Sidebar from "../components/sidebar";
import Footer from "../components/footer";

export default function PrivateRoute({ children }) {
  if (!isAuthenticated()) {
    <Navigate to="/login" />;
  }
  return (
    <>
      <Header />
      <Sidebar />
      {children}
      <Footer />
    </>
  );
}
