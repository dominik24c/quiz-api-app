import Navbar from './components/Navbar';
import Footer from './components/Footer';
import React from 'react';
import ReactDOM from 'react-dom';
import {Switch, Route} from 'react-router-dom';

const App = ()=> {
  return (
    <React.Fragment>
      {ReactDOM.createPortal(<Navbar/>,document.getElementById('navbar'))}
      {ReactDOM.createPortal(<Footer/>,document.getElementById('footer'))}
      <h2>Quiz app</h2>
        <Switch>
            <Route path="/" exact>
                <h1>Homepage</h1>
            </Route>
            <Route path="/login">
                <h1>Login</h1>
            </Route>
            <Route path="/sign-up">
                <h1>Sing up</h1>
            </Route>
            <Route path="/logout">
                <h1>Logout</h1>
            </Route>
        </Switch>
    </React.Fragment>
  );
}

export default App;
