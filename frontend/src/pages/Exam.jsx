import {useState, useEffect} from "react";
// import axios from "axios";
import api from "../api/token.js"

export default function Exam(props) {
    const [questions, setquestions] = useState([]);
    const [selectedAnswer, setSelectedAnswer] = useState({});
    useEffect( () => {
        api
        .get(`${process.env.REACT_APP_API_URL}/questions/`)
        .then(res => setquestions(res.data))
        .catch(err => console.error(err))
    },[]);

    const handleSelection = (questionId,answerId) => {
        setSelectedAnswer(prev => ({
            ...prev,
            [questionId]:answerId
        }));
        console.log(questionId);
        console.log(answerId);
    }
    
    const handleSubmission = async (e) => {
        e.preventDefault();
        try {
            const payload = {
            answers: Object.entries(selectedAnswer).map(([question, selected_answer]) => ({
                question,
                selected_answer
            }))
            };

            const res = await api.post(
                `${process.env.REACT_APP_API_URL}/questions/submit-test/`,
                payload
            );

            console.log('Submitted successfully:', res.data);
            alert('Test submitted successfully!');
            setSelectedAnswer({});
        } catch (err) {
            console.error('Submission failed:', err);
            alert('Submission failed');
        }
    };

    return <div id="testContainer">
        <form method="post"  onSubmit={handleSubmission}>
            <h1>Test</h1>
            <div>
                {questions.map((question)=>(
                    <div key={question.uid} className="question-block">
                        <h3>{question.question}</h3>
                        {question.question_answer.map((answer) => (
                            <label key={answer.uid}>
                                <input 
                                type="radio" 
                                name={`question-${question.uid}`} 
                                value={answer.uid} 
                                checked={selectedAnswer[question.uid] === answer.uid}
                                onChange={() => handleSelection(question.uid,answer.uid)}/>
                                {answer.answer}
                            </label>
                        ))}
                    </div>
                ))}
            </div>
            <button type="submit">Submit</button>
        </form>
    </div>
}