import React from "react";
import dateFormat from "dateformat";
import {useHistory} from "react-router-dom";

const Quiz = (props) => {
    const history = useHistory();
    const solveQuiz = () => {
        history.replace(`/quizzes/${props.id}`);
    }

    const formatDate = (date) => {
        const dateObj = new Date(date);
        return dateFormat(dateObj, 'hh:MM:ss dd.mm.yyyy');
    }

    return (
        <div className="quiz">
            <h2>{props.title}</h2>
            <p>{props.description}</p>
            <p>category: <b>{props.category}</b></p>
            <p>questions: <b>{props.num_of_questions}</b></p>
            <p>created by: {props.creator}</p>
            <i>{formatDate(props.created_at)}</i>
            <br/>
            <button onClick={solveQuiz}>Solve</button>
        </div>

    );
}

export default Quiz