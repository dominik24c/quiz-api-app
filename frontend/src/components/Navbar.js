import React, {useContext} from "react";
import QuizIcon from '../quiz.png';
import classes from './Navbar.module.css';
import {NavLink} from "react-router-dom";
import AuthContext from "../context/AuthContext";
import LogoutBtn from './auth/LogoutBtn';

const Navbar = () => {
    const authContext = useContext(AuthContext);

    return (
        <React.Fragment>
            <div className={classes.brand}>
                <NavLink to="/">
                    <img src={QuizIcon} alt="quiz icon"/>
                </NavLink>
            </div>
            <nav>
                <ul className={classes.links}>
                    {!authContext.isLoggedIn &&
                    <React.Fragment>
                        <li className={classes.link}>
                            <NavLink to="/login">Login</NavLink>
                        </li>
                        <li className={classes.link}>
                            <NavLink to="/sign-up">Sign up</NavLink>
                        </li>
                    </React.Fragment>
                    }
                    {
                        authContext.isLoggedIn &&
                        <React.Fragment>
                            <li className={classes.link}>
                                <NavLink to="/quizzes">Quizzes</NavLink>
                            </li>
                            <li className={classes.link}>
                                <NavLink to="/quizzes/create">Create Quiz</NavLink>
                            </li>
                            <li className={classes.link}>
                                <NavLink to="/logout">
                                    <LogoutBtn/>
                                </NavLink>
                            </li>
                        </React.Fragment>
                    }
                </ul>
            </nav>
        </React.Fragment>
    );
}

export default Navbar;