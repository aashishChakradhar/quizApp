import { useState, useEffect } from "react";
import axios from "axios";
export default function Signup(props) {
  const [info, setInfo] = useState({});
  const handleChange = (e) => {
    setInfo((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };
  async function handleSubmit(e) {
    e.preventDefault();
    try {
      await axios.post(`${process.env.REACT_APP_API_URL}/register/`, info);
      alert("User Created Successfully");
      setInfo({});
    } catch (error) {
      if (error.response && error.response.data) {
        const data = error.response.data;
        // Convert error object into readable string
        let messages = [];
        for (const key in data) {
          if (Array.isArray(data[key])) {
            messages.push(`${key}: ${data[key].join(", ")}`);
          } else {
            messages.push(`${key}: ${data[key]}`);
          }
        }
        alert("Registration Failed:\n" + messages.join("\n"));
      } else {
        alert("Registration Failed: " + error.message);
      }
    }
  }
  return (
    <form method="post" onSubmit={handleSubmit}>
      <label htmlFor="first_name">
        <input
          type="text"
          name="first_name"
          id="first_name"
          placeholder="First Name"
          value={info.first_name || ""}
          onChange={handleChange}
        />
      </label>
      <label htmlFor="last_name">
        <input
          type="text"
          name="last_name"
          id="last_name"
          placeholder="Last Name"
          value={info.last_name || ""}
          onChange={handleChange}
        />
      </label>
      <label htmlFor="email">
        <input
          type="email"
          name="email"
          id="email"
          placeholder="example@email.com"
          value={info.email || ""}
          onChange={handleChange}
        />
      </label>
      <label htmlFor="username">
        <input
          type="text"
          name="username"
          id="username"
          placeholder="username"
          value={info.username || ""}
          onChange={handleChange}
        />
      </label>
      <label htmlFor="password">
        <input
          type="password"
          name="password"
          id="password"
          placeholder="password"
          value={info.password || ""}
          onChange={handleChange}
        />
      </label>
      <label htmlFor="password2">
        <input
          type="password"
          name="password2"
          id="password2"
          placeholder="confirm password"
          value={info.password2 || ""}
          onChange={handleChange}
        />
      </label>
      <button type="submit">Signup</button>
    </form>
  );
}
