import React, { useState, useEffect } from "react";
import axios from "axios";
export default function Category(props) {
  const [category, setCategory] = useState([]);
  useEffect(() => {
    axios
      .get(`${process.env.REACT_APP_API_URL}/categories/`)
      .then((res) => setCategory(res.data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div id="display-container">
      <h1>Category</h1>
      <ul>
        {category.map((cat) => (
          <li key={cat.uid}>{cat.category_name}</li>
        ))}
      </ul>
    </div>
  );
}
