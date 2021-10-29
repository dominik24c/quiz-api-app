import React, {Fragment, useCallback, useContext, useEffect, useState} from "react";
import AuthContext from "../../context/AuthContext";

import Quiz from "./Quiz";

const Quizzes = (props) => {
    const authContext = useContext(AuthContext);
    const [quizzes, setQuizzes] = useState([])
    const fetchQuizzes = useCallback(async () => {
        let quizzesObjects = [];

        try {
            const response = await fetch(`${URL}/api/quizzes/`, {
                method: 'GET',
                headers: {
                    "Authorization": `JWT ${authContext.token}`
                }
            });

            const data = await response.json();
            quizzesObjects = data['quizzes']
        } catch (error) {
            console.log(error);
        }
        // console.log(quizzesObjects);
        const quizzes = quizzesObjects.map(quiz => {
            return (<Quiz key={quiz.id}
                          id={quiz.id}
                          title={quiz.title}
                          description={quiz.description}
                          category={quiz.category}
                          creator={quiz.owner}
                          created_at={quiz.created_at}
                          num_of_questions={quiz.num_of_questions}
            />)
        });
        // console.log(quizzes)
        setQuizzes(quizzes);
    },[authContext.token]);

    useEffect(() => {
        fetchQuizzes();
    }, [fetchQuizzes]);

    return (
        <Fragment>
            <h1>Quizzes</h1>
            {quizzes && (<div className="quizzes">
                {quizzes}
            </div>)}
        </Fragment>
    );
}

export default Quizzes;