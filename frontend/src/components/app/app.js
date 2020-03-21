import React from 'react';
import logo from './logo.svg';
import './App.scss';
import SignIn from '../signIn/signIn';
import UserArea from '../userArea/userArea';
import AddSurvey from '../addSurvey/addSurvey';
import Navigation from '../navigation/navigation';

function App() {
    return (
        <div className="App">
            Crimpit
            <AddSurvey />
            <div></div>
        </div>
    );
}

export default App;
