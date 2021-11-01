import React, {Fragment, useCallback, useContext, useEffect, useRef, useState} from "react";
import AuthContext from "../../context/AuthContext";

import Quiz from "./Quiz";
import Category from "./Category";

const Quizzes = (props) => {
    const authContext = useContext(AuthContext);
    const [quizzes, setQuizzes] = useState([]);

    const searchedPhraseRef = useRef();
    const [searchedPhrase, setSearchedPhrase] = useState('');
    const [searchedCategory, setSearchedCategory] = useState('');
    const [sortByDate, setSortByDate] = useState(false);

    const fetchQuizzes = useCallback(async (searchedPhrase, searchedCategory,sortByDate) => {
        let quizzesObjects = [];

        try {
            let url = `${URL}/api/quizzes/`;

            if (searchedPhrase) {
                url += `?search=${searchedPhrase}`;
            }

            if (searchedCategory) {
                if (url.includes('?')) {
                    url += `&category=${searchedCategory}`;

                } else {
                    url += `?category=${searchedCategory}`;
                }
            }
            if (sortByDate) {
                if (url.includes('?')) {
                    url += `&sort_by_date=${sortByDate}`;

                } else {
                    url += `?sort_by_date=${sortByDate}`;
                }
            }

            const response = await fetch(url, {
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

        setQuizzes(quizzesObjects);
    }, [authContext.token]);

    useEffect(() => {
        fetchQuizzes(searchedPhrase, searchedCategory,sortByDate);
    }, [searchedPhrase, searchedCategory, sortByDate, fetchQuizzes])

    const searchQuizzes = (event) => {
        event.preventDefault();
        setSearchedPhrase(searchedPhraseRef.current.value);
    }

    const selectCategoryHandler = (event) => {
        setSearchedCategory(event.target.value);
    }

    const sortByDateQuizzes = (event) => {
        console.log(sortByDate)
        setSortByDate(!sortByDate);
    }

    return (
        <Fragment>
            <h1>Quizzes</h1>
            <form onSubmit={searchQuizzes.bind(this)}>
                <input type="text" name="search" id="search" required
                       ref={searchedPhraseRef}/>
                <button type="submit">Search</button>
            </form>
            <Category selectCategory={selectCategoryHandler.bind(this)}/>
            <div>
                <button onClick={sortByDateQuizzes}>sort by date</button>
            </div>
            {quizzes.length > 0 && (<div className="quizzes">
                {quizzes.map(quiz => {
                    return (<Quiz key={quiz.id}
                                  id={quiz.id}
                                  title={quiz.title}
                                  description={quiz.description}
                                  category={quiz.category}
                                  creator={quiz.owner}
                                  created_at={quiz.created_at}
                                  num_of_questions={quiz.num_of_questions}
                    />)
                })}
            </div>)}
            {quizzes.length === 0 && <h2>Not Found Quizzes</h2>}
        </Fragment>
    );
}

export default Quizzes;