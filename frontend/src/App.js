import React, {useContext} from 'react';
import ReactDOM from 'react-dom';
import {Redirect, Route, Switch} from 'react-router-dom';

import LoginForm from "./components/auth/LoginForm";
import Navbar from './components/Navbar';
import Footer from './components/Footer';

import AuthContext from "./context/AuthContext";
import SignUpForm from "./components/auth/SignUpForm";
import Quizzes from "./components/quiz/Quizzes";
import SolveQuiz from "./components/quiz/SolveQuiz";
import CreateQuiz from "./components/quiz/CreateQuiz";


const App = () => {
    const authContext = useContext(AuthContext)

    return (
        <React.Fragment>
            {ReactDOM.createPortal(<Navbar/>, document.getElementById('navbar'))}
            {ReactDOM.createPortal(<Footer/>, document.getElementById('footer'))}
            {/*<h2>Quiz app</h2>*/}
            <Switch>
                <Route path="/" exact>
                    <h1>Homepage</h1>
                </Route>
                {!authContext.isLoggedIn &&
                <Route path="/login">
                    <LoginForm/>
                </Route>
                }
                {!authContext.isLoggedIn &&
                <Route path="/sign-up">
                    <SignUpForm/>
                </Route>
                }
                {authContext.isLoggedIn &&
                <Route path="/quizzes" exact>
                    <Quizzes/>
                </Route>
                }
                {authContext.isLoggedIn &&
                <Route path="/quizzes/create">
                    <CreateQuiz/>
                </Route>
                }
                {authContext.isLoggedIn &&
                <Route path="/quizzes/:id">
                    <SolveQuiz/>
                </Route>
                }
                {authContext.isLoggedIn &&
                <Route path="/logout">
                    <CreateQuiz/>
                </Route>
                }
                {authContext.isLoggedIn &&
                <Route path="/logout">
                    <h1>Logout</h1>
                </Route>
                }
                <Route path="*">
                    <Redirect to="/"/>
                </Route>
            </Switch>
        </React.Fragment>
    );
}

export default App;
