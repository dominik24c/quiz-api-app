import React from "react";
import QuizIcon from '../quiz.png';
import classes from './Navbar.module.css';

const Navbar = () => {
    return(
        <React.Fragment>
            <div className={classes.brand}>
                <a href="# ">
                    <img src={QuizIcon} alt="quiz icon"/>
                </a>
            </div>
            <nav>
                <ul className={classes.links}>
                    <li className={classes.link}><a href="#">Login</a></li>
                    <li className={classes.link}><a href="#">Sign up</a></li>
                    <li className={classes.link}><a href="#">Logout</a></li>
                </ul>
            </nav>
        </React.Fragment>
    );
}

export default Navbar;