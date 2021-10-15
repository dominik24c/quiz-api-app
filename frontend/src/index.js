import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import {BrowserRouter} from "react-router-dom";
import {AuthContextProvider} from "./context/AuthContext";

const URL = ' http://127.0.0.1:8000'
global.URL = URL;

ReactDOM.render(
    <AuthContextProvider>
        <BrowserRouter>
            <App/>
        </BrowserRouter>
    </AuthContextProvider>,
    document.getElementById('root')
);