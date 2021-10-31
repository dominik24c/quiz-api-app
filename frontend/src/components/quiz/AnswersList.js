import Answer from "./Answer";
import {useCallback, useEffect, useState} from "react";

const ANSWERS_MIN_LENGTH = 2;
const ANSWERS_MAX_LENGTH = 4;

const AnswersList = () => {
    const [answers, setAnswers] = useState([]);

    const addAnswers = (event) => {
        event.preventDefault();
        const lastElement = answers[answers.length - 1];
        setAnswers([...answers, {key: lastElement.key + 1}])
    };

    const initAnswers = useCallback(() => {
        const answersArr = [];
        for (let i = 0; i < ANSWERS_MIN_LENGTH; i++) {
            answersArr.push({key: i})
        }
        setAnswers(answersArr);
    }, [])

    useEffect(() => {
        initAnswers();
    }, [initAnswers])

    return (
        <div className="answers">
            {answers.map(a => <Answer key={a.key}/>)}
            {answers.length < ANSWERS_MAX_LENGTH &&
            < button type="click" onClick={addAnswers.bind(this)}>
                Add answer
            </button>
            }
        </div>
    );
}

export default AnswersList;