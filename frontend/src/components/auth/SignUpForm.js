import React, {useContext, useRef, useState} from "react";
import {useHistory} from "react-router-dom";
import AuthContext from "../../context/AuthContext";

const SignUpForm = () => {
    const emailRef = useRef();
    const usernameRef = useRef();
    const passwordRef = useRef();
    const history = useHistory();
    const authContext = useContext(AuthContext);

    const [usernameError, setUsernameError] = useState('');
    const [passwordError, setPasswordError] = useState('');

    const registerUser = async (event) => {
        event.preventDefault();

        if (validateForm()) {

            try {
                const response = await fetch(`${URL}/api/auth/register`, {
                    method: 'POST',
                    headers: {
                        'Content-type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: usernameRef.current.value,
                        email: emailRef.current.value,
                        password: passwordRef.current.value,
                    })
                });

                const data = await response.json();
                if (response.status === 400) {
                    if (data && data.username) {
                        setUsernameError(data.username[0]);
                    }
                }
                // console.log(data);
                else if (response.status ===200) {
                    //login
                    const token = data.token;
                    const expirationTime = new Date(new Date().getTime() + (+data.expired * 1000));
                    authContext.login(token, expirationTime.toISOString());
                    history.replace('/quizzes');
                }


            } catch (error) {
                console.log(error);
            }
        }
    }

    const validateForm = () => {
        return validateUsername() && validatePassword();
    }
    const validatePassword = () => {
        const password = passwordRef.current.value;
        let isValidated = true;

        if (!/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])/.test(password)) {
            setPasswordError('The password must contain at least one digit, upper case letter and lower case letter!');
            isValidated = false;
        }

        if (password.length < 8) {
            setPasswordError('The password must be at least 8 characters!');
            isValidated = false;
        }

        return isValidated;
    }

    const validateUsername = () => {
        const username = usernameRef.current.value;
        const isValidated = username.length < 5
        if (isValidated) {
            setUsernameError('The username must be at least 5 characters!');
        }
        return !isValidated;
    }

    return (
        <form onSubmit={registerUser}>
            {usernameError && <div>
                {usernameError}
            </div>}
            <div>
                <label htmlFor="username">Username: </label>
                <input type="text" name="username" ref={usernameRef} required
                       onChange={() => setUsernameError('')}/>
            </div>
            <div>
                <label htmlFor="email">Email: </label>
                <input type="email" name="email" ref={emailRef} required/>
            </div>
            {passwordError && <div>
                {passwordError}
            </div>}
            <div>
                <label htmlFor="password">Password: </label>
                <input type="password" name="password" ref={passwordRef} required
                       onChange={() => setPasswordError('')}/>
            </div>
            <button type="submit">Register</button>
        </form>
    );
}

export default SignUpForm;