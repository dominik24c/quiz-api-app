import Navbar from './components/Navbar';
import Footer from './components/Footer';
import React from 'react';
import ReactDOM from 'react-dom';

const App = ()=> {
  return (
    <React.Fragment>
      {ReactDOM.createPortal(<Navbar/>,document.getElementById('navbar'))}
      {ReactDOM.createPortal(<Footer/>,document.getElementById('footer'))}
      <h2>Quiz app</h2>
    </React.Fragment>
  );
}

export default App;
