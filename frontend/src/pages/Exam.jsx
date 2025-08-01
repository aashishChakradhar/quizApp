import {useState, useEffect} from "react";
import axios from "axios";

export default function Exam(props) {
    const [queries, setQueries] = useState([]);
    const [selectedAnswer, setSelectedAnswer] = useState({});
    useEffect( () => {
        axios.get(`${process.env.REACT_APP_API_URL}/questions/`)
        .then(res => setQueries(res.data))
        .catch(err => console.error(err))
    },[]);
    
    return <div id="testContainer">
        <h1>Test</h1>
        <div>
            {queries.map((query)=>(
                <div key={query.uid} className="question-block">
                    <h3>{query.question}</h3>
                    {query.question_answer.map((answer) => (
                        <label key={answer.uid}>
                            <input type="radio" name={`question-${query.uid}`} value={answer.uid} />
                            {answer.answer}
                        </label>
                    ))}
                </div>
            ))}
        </div>
    </div>
}