import {useCallback, useContext, useEffect, useState} from "react";

import AuthContext from "../../context/AuthContext";
import QuestionList from "./QuestionList";

const CreateQuiz = () => {
    const authContext = useContext(AuthContext)
    const [categories, setCategories] = useState([]);

    const getCategories = useCallback(async () => {
        try {
            const response = await fetch(`${URL}/api/quizzes/categories/`, {
                method: "GET",
                headers: {
                    "Authorization": `JWT ${authContext.token}`
                }
            });
            const data = await response.json()

            const categoriesList = data['categories']
            const categoriesJSX = categoriesList.map(category => {
                return (
                    <option key={category} value={category}>{category}</option>
                )
            })
            setCategories(categoriesJSX);
        } catch (e) {
            console.log(e);
        }

    }, []);

    useEffect(() => {
        getCategories();
    }, [getCategories])

    const createQuiz = (event)=>{
        event.preventDefault();
    }
    return (
        <div id="quiz">
            <h2>Create Quiz</h2>
            <form onSubmit={createQuiz.bind(this)}>
                <div>
                    <label htmlFor="title">Title: </label>
                    <input type="text" name="title" id="title"/>
                </div>
                <div>
                    <label htmlFor="description">Description: </label>
                    <textarea name="description" id="description"/>
                </div>
                <div>
                    <label htmlFor="category">Category:</label>
                    <select name="category" id="category">
                        {categories}
                    </select>
                </div>
                <QuestionList/>
                <button type="submit">Create</button>
            </form>
        </div>
    );
}

export default CreateQuiz;