import React from "react";
import QuizIcon from '../quiz.png';
import classes from './Navbar.module.css';
import {NavLink} from "react-router-dom";

const Navbar = () => {
    return(
        <React.Fragment>
            <div className={classes.brand}>
                <NavLink to="/">
                    <img src={QuizIcon} alt="quiz icon"/>
                </NavLink>
            </div>
            <nav>
                <ul className={classes.links}>
                    <li className={classes.link}>
                        <NavLink to="/login">Login</NavLink>
                    </li>
                    <li className={classes.link}>
                        <NavLink to="/sign-up">Sign up</NavLink>
                    </li>
                    <li className={classes.link}>
                        <NavLink to="/logout">Logout</NavLink>
                    </li>
                </ul>
            </nav>
        </React.Fragment>
    );
}

export default Navbar;