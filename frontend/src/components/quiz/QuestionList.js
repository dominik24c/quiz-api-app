import Question from "./Question";
import {useCallback, useEffect, useState} from "react";

const QUESTIONS_MIN_LENGTH = 3;
const QUESTIONS_MAX_LENGTH = 20;


const QuestionList = (props) => {
    const [questions, setQuestions] = useState([]);

    const initQuestions = useCallback(() => {
        const questionsArr = [];
        for (let i = 0; i < QUESTIONS_MIN_LENGTH; i++) {
            questionsArr.push({key: i});
        }
        setQuestions(questionsArr);
    }, []);

    useEffect(() => {
        initQuestions();
    }, [initQuestions])

    const addQuestion = (event) => {
        event.preventDefault();
        const lastElement = questions[questions.length - 1];
        setQuestions([...questions, {key: lastElement.key + 1}])
    }

    return (
        <div id="questions">
            {
                questions.map(q => <Question key={q.key}/>)
            }
            {   questions.length <= QUESTIONS_MAX_LENGTH &&
                <button id="add-question-btn" onClick={addQuestion.bind(this)}>+</button>
            }
        </div>
    )
}

export default QuestionList;
