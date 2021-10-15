import React, {useContext, useState} from "react";
import {useHistory} from 'react-router-dom';
import AuthContext from "../../context/AuthContext";

const LoginForm = () => {
    const authContext = useContext(AuthContext);
    const history = useHistory();

    const [error, setError] = useState(null);

    const loginHandler = async (event) => {
        event.preventDefault();
        // console.log(event.target.value)
        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');
        // console.log(usernameInput.value, passwordInput.value)

        try {
            const response = await fetch(`${URL}/api/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: usernameInput.value,
                    password: passwordInput.value,
                })
            })
            const data = await response.json();
            // console.log(data);
            if (data) {
                const errors = data.non_field_errors;
                if (errors) {
                    // console.log(errors[0])
                    setError(errors[0]);
                } else {
                    setError(null);
                    const token = data.token;
                    const expirationTime = new Date(new Date().getTime() + (+data.expired * 1000));

                    authContext.login(token, expirationTime.toISOString());
                    history.replace('/quizzes');

                }
            }
        } catch (error) {
            console.log(error);
        }
    };

    const resetError = () => {
        setError(null);
    }

    return (
        <>
            {error &&
            (<div>
                {error}
            </div>)
            }
            <form onSubmit={loginHandler}>
                <div>
                    <label htmlFor="username">Username:</label>
                    <input type="text" name="username" id="username" onChange={resetError} required/>
                </div>
                <div>
                    <label htmlFor="password">Password:</label>
                    <input type="password" name="password" id="password" onChange={resetError} required/>
                </div>
                <button type="submit">Login</button>
            </form>
        </>
    );
}

export default LoginForm;