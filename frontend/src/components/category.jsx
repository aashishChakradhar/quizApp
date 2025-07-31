import {useState, useEffect} from "react";
import axios from "axios";

function Category(props){
    const [categories,setCategories] = useState([]);

    useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}/categories/`)
      .then(res => setCategories(res.data))
      .catch(err => console.error(err));
  }, []);
    
    return <div>
      <h1>Categories</h1>
      <ul>
        {categories.map(cat => (
          <li key={cat.uid}>{cat.category_name}</li>
        ))}
      </ul>
    </div>
}
export default Category;