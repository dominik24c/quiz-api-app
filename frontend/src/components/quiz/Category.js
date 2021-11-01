import {useCallback, useContext, useEffect, useState} from "react";
import AuthContext from "../../context/AuthContext";

const Category = (props) => {
    const authContext = useContext(AuthContext);
    const [categories, setCategories] = useState([]);
    // const category = useRef();

    const getCategories = useCallback(async () => {
        try {
            const response = await fetch(`${URL}/api/quizzes/categories/`, {
                method: "GET",
                headers: {
                    "Authorization": `JWT ${authContext.token}`
                }
            });
            const data = await response.json()
            setCategories(data['categories']);
        } catch (e) {
            console.log(e);
        }

    }, []);

    useEffect(() => {
        getCategories();
    }, [getCategories])
    return (
        <div>
            <label htmlFor="category">Category:</label>
            <select name="category" id="category" onChange={props.selectCategory}>
                {categories.map(category => {
                    return (
                        <option key={category} value={category}>{category}</option>
                    )
                })}
            </select>
        </div>
    )
}

export default Category;