import { Link } from "react-router-dom";
export default function Header(props) {
  const greeting =
    new Date().getHours() < 12
      ? "Good Morning"
      : new Date().getHours() < 16
      ? "Good Afternoon"
      : "Good Evening";
  return (
    <header>
      <Link id="title" to="/dashboard">
        Quizzy Quiz
      </Link>
      <div id="greeting">
        {greeting},{props.user}
      </div>
    </header>
  );
}
